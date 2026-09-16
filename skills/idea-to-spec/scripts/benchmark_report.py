#!/usr/bin/env python3
"""Summarize normalized paired benchmark results and evaluate release thresholds."""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path


def average(values: list[float]) -> float | None:
    return round(statistics.fmean(values), 4) if values else None


def summarize(manifest: dict, results: dict) -> dict:
    cases = {row["id"]: row for row in manifest.get("cases", [])}
    dimensions = manifest.get("dimensions", [])
    rows = results.get("results", [])
    variants = {}
    repetitions = int(manifest.get("repetitions", 1))
    expected_keys = {(case_id, repetition) for case_id in cases for repetition in range(1, repetitions + 1)}
    matrix_issues = {}
    for variant in ("baseline", "plugin"):
        selected = [row for row in rows if row.get("variant") == variant]
        keys = [(row.get("case_id"), row.get("repetition")) for row in selected]
        duplicates = sorted({key for key in keys if keys.count(key) > 1}, key=str)
        missing_keys = sorted(expected_keys - set(keys), key=str)
        extra_keys = sorted(set(keys) - expected_keys, key=str)
        matrix_issues[variant] = {"missing": missing_keys, "duplicates": duplicates, "unexpected": extra_keys}
        critical_failures = sum(bool(row.get("critical_failure")) or (bool(cases.get(row.get("case_id"), {}).get("critical")) and not bool(row.get("passed"))) for row in selected)
        variants[variant] = {
            "runs": len(selected),
            "pass_rate": average([1.0 if row.get("passed") else 0.0 for row in selected]),
            "critical_failures": critical_failures,
            "scores": {dimension: average([float(row.get("scores", {}).get(dimension)) for row in selected if dimension in row.get("scores", {})]) for dimension in dimensions},
            "cost_usd": round(sum(float(row.get("cost_usd", 0)) for row in selected), 4),
        }
    expected = len(cases) * repetitions
    missing = {variant: expected - variants[variant]["runs"] for variant in variants}
    plugin_pass = variants["plugin"]["pass_rate"]
    baseline_pass = variants["baseline"]["pass_rate"]
    improvement = round(plugin_pass - baseline_pass, 4) if plugin_pass is not None and baseline_pass is not None else None
    thresholds = manifest.get("thresholds", {})
    blockers = []
    if any(value != 0 for value in missing.values()) or any(issue for variant in matrix_issues.values() for issue in variant.values()):
        blockers.append("INCOMPLETE_RUN_MATRIX")
    if plugin_pass is None or plugin_pass < thresholds.get("plugin_pass_rate_min", 0):
        blockers.append("PLUGIN_PASS_RATE")
    for dimension, threshold_key in (("activation", "activation_score_min"), ("gates", "gates_score_min"), ("security", "security_score_min")):
        value = variants["plugin"]["scores"].get(dimension)
        if value is None or value < thresholds.get(threshold_key, 0):
            blockers.append(f"{dimension.upper()}_SCORE")
    if variants["plugin"]["critical_failures"] > thresholds.get("critical_failures_max", 0):
        blockers.append("CRITICAL_FAILURES")
    if improvement is None or improvement < thresholds.get("improvement_over_baseline_min", 0):
        blockers.append("BASELINE_IMPROVEMENT")
    unknown_cases = sorted({row.get("case_id") for row in rows} - set(cases))
    if unknown_cases:
        blockers.append("UNKNOWN_CASES")
    return {"schema_version": "1.0", "suite": manifest.get("suite"), "release_gate": "PASS" if not blockers else "FAIL", "blockers": sorted(set(blockers)), "expected_runs_per_variant": expected, "missing_runs": missing, "matrix_issues": matrix_issues, "variants": variants, "improvement_over_baseline": improvement, "unknown_cases": unknown_cases}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("results", type=Path)
    parser.add_argument("--allow-incomplete", action="store_true")
    args = parser.parse_args(argv)
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        results = json.loads(args.results.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 1
    report = summarize(manifest, results)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["release_gate"] == "PASS" or args.allow_incomplete else 2


if __name__ == "__main__":
    sys.exit(main())
