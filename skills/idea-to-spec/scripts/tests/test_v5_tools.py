#!/usr/bin/env python3
"""Tests for V5 evaluation and security tools."""

from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


SCRIPTS = Path(__file__).resolve().parents[1]
PACKAGE = SCRIPTS.parents[2]
EVALS = load("validate_evals", SCRIPTS / "validate_evals.py")
BENCHMARK = load("benchmark_report", SCRIPTS / "benchmark_report.py")
SECURITY = load("security_audit", SCRIPTS / "security_audit.py")


class V5ToolsTests(unittest.TestCase):
    def test_final_metadata_and_bilingual_readmes(self) -> None:
        manifest = json.loads((PACKAGE / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], "5.0.1")
        self.assertEqual(manifest["author"]["name"], "SIELINOU GAMENI Sylvain Junior")
        self.assertIn("SIELINOU GAMENI Sylvain Junior", (PACKAGE / "README.md").read_text(encoding="utf-8"))
        self.assertIn("SIELINOU GAMENI Sylvain Junior", (PACKAGE / "README.fr.md").read_text(encoding="utf-8"))

    def test_bilingual_readmes_cover_all_agents_and_tools(self) -> None:
        readmes = [(PACKAGE / name).read_text(encoding="utf-8") for name in ("README.md", "README.fr.md")]
        names = [path.stem for path in (PACKAGE / "agents").glob("*.md")]
        tools = [path.name for path in (PACKAGE / "skills/idea-to-spec/scripts").glob("*.py") if path.name != "__init__.py"]
        for readme in readmes:
            for name in names:
                self.assertIn(name, readme)
            for tool in tools:
                self.assertIn(tool, readme)

    def test_bilingual_readmes_include_three_mermaid_diagrams(self) -> None:
        for name in ("README.md", "README.fr.md"):
            text = (PACKAGE / name).read_text(encoding="utf-8")
            self.assertEqual(text.count("```mermaid"), 3)
            blocks = text.split("```mermaid")[1:]
            self.assertTrue(all("```" in block for block in blocks))
            self.assertIn("flowchart TD", blocks[0])
            self.assertIn("stateDiagram-v2", blocks[1])
            self.assertIn("flowchart LR", blocks[2])

    def test_packaged_eval_suite_is_valid(self) -> None:
        self.assertEqual(EVALS.validate(PACKAGE / "evals"), [])

    def test_eval_validator_rejects_missing_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "case/graders").mkdir(parents=True)
            (root / "case/prompt.md").write_text("# Prompt\nA sufficiently long test prompt.", encoding="utf-8")
            (root / "case/graders/behavior.md").write_text("PASS or FAIL", encoding="utf-8")
            (root / "BENCHMARK_MANIFEST.json").write_text(json.dumps({"schema_version": "1.0", "variants": ["baseline", "plugin"], "repetitions": 1, "dimensions": ["gates"], "thresholds": {}, "cases": [{"id": "case", "language": "fr", "sector": "x", "profile": "lean", "complexity": "small", "critical": False}]}), encoding="utf-8")
            self.assertTrue(EVALS.validate(root))

    def test_benchmark_gate_passes_complete_improvement(self) -> None:
        dimensions = ["activation", "gates", "security"]
        manifest = {"suite": "test", "repetitions": 1, "dimensions": dimensions, "thresholds": {"plugin_pass_rate_min": 1, "activation_score_min": 1, "gates_score_min": 1, "security_score_min": 1, "critical_failures_max": 0, "improvement_over_baseline_min": 1}, "cases": [{"id": "a"}]}
        results = {"results": [
            {"case_id": "a", "variant": "baseline", "repetition": 1, "passed": False, "critical_failure": False, "scores": {key: 0 for key in dimensions}},
            {"case_id": "a", "variant": "plugin", "repetition": 1, "passed": True, "critical_failure": False, "scores": {key: 1 for key in dimensions}},
        ]}
        self.assertEqual(BENCHMARK.summarize(manifest, results)["release_gate"], "PASS")

    def test_benchmark_gate_blocks_incomplete_matrix(self) -> None:
        manifest = {"suite": "test", "repetitions": 1, "dimensions": [], "thresholds": {}, "cases": [{"id": "a"}]}
        report = BENCHMARK.summarize(manifest, {"results": []})
        self.assertIn("INCOMPLETE_RUN_MATRIX", report["blockers"])

    def test_benchmark_gate_blocks_duplicate_matrix_rows(self) -> None:
        manifest = {"suite": "test", "repetitions": 1, "dimensions": [], "thresholds": {}, "cases": [{"id": "a"}]}
        row = {"case_id": "a", "variant": "plugin", "repetition": 1, "passed": True, "critical_failure": False, "scores": {}}
        report = BENCHMARK.summarize(manifest, {"results": [row, dict(row)]})
        self.assertIn("INCOMPLETE_RUN_MATRIX", report["blockers"])

    def test_package_security_audit_is_clean(self) -> None:
        self.assertEqual(SECURITY.audit(PACKAGE), [])

    def test_security_audit_detects_secret_and_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fake_secret = "sk-" + "abcdefghijklmnopqrstuvwxyz123456"
            (root / "bad.txt").write_text(fake_secret, encoding="utf-8")
            (root / "link").symlink_to(root / "bad.txt")
            codes = {item["code"] for item in SECURITY.audit(root)}
            self.assertTrue({"OPENAI_KEY", "SYMLINK"}.issubset(codes))


if __name__ == "__main__":
    unittest.main()
