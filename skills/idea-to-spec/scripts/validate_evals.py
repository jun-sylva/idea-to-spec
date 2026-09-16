#!/usr/bin/env python3
"""Validate the local Claude Code plugin eval suite without model calls."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def frontmatter(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text
    try:
        raw, body = text[4:].split("\n---\n", 1)
    except ValueError:
        return {}, text
    data = {}
    for line in raw.splitlines():
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.+?)\s*$", line)
        if match:
            data[match.group(1)] = match.group(2).strip("'\"")
    return data, body


def validate(root: Path) -> list[dict[str, str]]:
    findings = []
    manifest_path = root / "BENCHMARK_MANIFEST.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return [{"severity": "ERROR", "code": "MANIFEST", "message": str(exc)}]
    expected = {case.get("id") for case in manifest.get("cases", []) if isinstance(case, dict)}
    if manifest.get("schema_version") != "1.0" or manifest.get("variants") != ["baseline", "plugin"]:
        findings.append({"severity": "ERROR", "code": "MANIFEST_FORMAT", "message": "schema_version ou variants invalide"})
    if not isinstance(manifest.get("repetitions"), int) or manifest.get("repetitions", 0) < 1:
        findings.append({"severity": "ERROR", "code": "MANIFEST_REPETITIONS", "message": "repetitions doit être positif"})
    dimensions = manifest.get("dimensions")
    if not isinstance(dimensions, list) or not dimensions or len(dimensions) != len(set(dimensions)):
        findings.append({"severity": "ERROR", "code": "MANIFEST_DIMENSIONS", "message": "dimensions absentes ou dupliquées"})
    actual = {path.name for path in root.iterdir() if path.is_dir() and path.name != "results"}
    for name in sorted(expected - actual):
        findings.append({"severity": "ERROR", "code": "CASE_MISSING", "message": name})
    for name in sorted(actual - expected):
        findings.append({"severity": "ERROR", "code": "CASE_UNDECLARED", "message": name})
    for name in sorted(actual):
        case = root / name
        prompt = case / "prompt.md"
        if not prompt.is_file() or len(prompt.read_text(encoding="utf-8").strip()) < 20:
            findings.append({"severity": "ERROR", "code": "PROMPT_INVALID", "message": name})
        graders = case / "graders"
        files = sorted(graders.glob("*.md")) if graders.is_dir() else []
        if not files:
            findings.append({"severity": "ERROR", "code": "GRADERS_MISSING", "message": name})
        types = set()
        for path in files:
            meta, body = frontmatter(path)
            kind = meta.get("type")
            types.add(kind)
            if kind not in {"llm", "tool_used"}:
                findings.append({"severity": "ERROR", "code": "GRADER_TYPE", "message": str(path.relative_to(root))})
            if kind == "llm":
                try:
                    valid_weight = float(meta.get("weight", "0")) > 0
                except ValueError:
                    valid_weight = False
                if not valid_weight or "PASS" not in body or "FAIL" not in body:
                    findings.append({"severity": "ERROR", "code": "LLM_GRADER_INVALID", "message": str(path.relative_to(root))})
            if kind == "tool_used" and (not meta.get("tool") or not meta.get("input_match")):
                findings.append({"severity": "ERROR", "code": "TOOL_GRADER_INVALID", "message": str(path.relative_to(root))})
        if "llm" not in types or "tool_used" not in types:
            findings.append({"severity": "ERROR", "code": "GRADER_COVERAGE", "message": name})
    case_rows = manifest.get("cases", [])
    ids = [row.get("id") for row in case_rows if isinstance(row, dict)]
    if len(ids) != len(set(ids)):
        findings.append({"severity": "ERROR", "code": "DUPLICATE_CASE", "message": "Identifiants dupliqués"})
    for field in ("language", "sector", "profile", "complexity", "critical"):
        if any(field not in row for row in case_rows if isinstance(row, dict)):
            findings.append({"severity": "ERROR", "code": "CASE_METADATA", "message": field})
    if not isinstance(manifest.get("thresholds"), dict):
        findings.append({"severity": "ERROR", "code": "MANIFEST_THRESHOLDS", "message": "thresholds absent"})
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evals", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)
    findings = validate(args.evals.expanduser().resolve())
    payload = {"valid": not findings, "errors": len(findings), "findings": findings}
    if args.as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for item in findings:
            print(f"{item['severity']} {item['code']}: {item['message']}")
        print(f"Eval validation: {len(findings)} error(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
