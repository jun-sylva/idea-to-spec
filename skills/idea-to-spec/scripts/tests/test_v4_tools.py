#!/usr/bin/env python3
"""Tests for V4 governance and lifecycle tools."""

from __future__ import annotations

import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


SCRIPTS = Path(__file__).resolve().parents[1]
BASELINE = load("baseline_manager", SCRIPTS / "baseline_manager.py")
COMPARE = load("compare_versions", SCRIPTS / "compare_versions.py")
METRICS = load("workflow_metrics", SCRIPTS / "workflow_metrics.py")
DASHBOARD = load("project_dashboard", SCRIPTS / "project_dashboard.py")


class V4ToolsTests(unittest.TestCase):
    def canonical_project(self, root: Path) -> None:
        files = {
            "MEMORY.md": "# Memory\n", "PROJECT.md": "# Project\n",
            "requirements/REQUIREMENTS.md": "# Requirements\n\n### FR-001 — Export\n",
            "planning/TASKS.md": "# Tasks\n\n### TASK-001 — Export\nCouvre FR-001 et TEST-001.\n",
            "decisions/DECISIONS.md": "# Decisions\n", "risks/RISK_REGISTER.md": "# Risks\n", "CHANGELOG.md": "# Changelog\n",
        }
        for relative, content in files.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    def test_baseline_create_and_verify(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.canonical_project(root)
            manifest = root / "baseline.json"
            self.assertEqual(BASELINE.main(["create", str(root), "--version", "1.0.0", "--project-name", "Demo", "--created-at", "2026-09-13T10:00:00Z", "--approval", "APR-001", "--output", str(manifest)]), 0)
            with redirect_stdout(io.StringIO()):
                self.assertEqual(BASELINE.main(["verify", str(root), str(manifest)]), 0)

    def test_baseline_detects_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.canonical_project(root)
            manifest = root / "baseline.json"
            BASELINE.main(["create", str(root), "--version", "1.0.0", "--project-name", "Demo", "--created-at", "2026-09-13T10:00:00Z", "--output", str(manifest)])
            (root / "PROJECT.md").write_text("changed", encoding="utf-8")
            with redirect_stdout(io.StringIO()):
                self.assertEqual(BASELINE.main(["verify", str(root), str(manifest)]), 2)

    def test_baseline_rejects_path_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            root = base / "project"
            root.mkdir()
            outside = base / "outside.txt"
            outside.write_text("private", encoding="utf-8")
            manifest = root / "baseline.json"
            manifest.write_text(json.dumps({"baseline_id": "BASELINE-1.0.0", "files": [{"path": "../outside.txt", "sha256": "0" * 64, "size": 7}]}), encoding="utf-8")
            with redirect_stdout(io.StringIO()):
                self.assertEqual(BASELINE.main(["verify", str(root), str(manifest)]), 2)

    def test_compare_reports_identifiers(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            old, new = root / "old.md", root / "new.md"
            old.write_text("### FR-001 — A\n", encoding="utf-8")
            new.write_text("### FR-002 — B\n", encoding="utf-8")
            result = COMPARE.compare(old, new)
            self.assertEqual(result["identifiers_added"], ["FR-002"])
            self.assertEqual(result["identifiers_removed"], ["FR-001"])

    def test_metrics_cycle_pending_scope_and_debt(self) -> None:
        payload = {"project": "Demo", "events": [
            {"event_id": "EVT-1", "type": "PHASE_STARTED", "occurred_at": "2026-09-13T10:00:00Z", "phase": "review", "version": "1.0.0", "data": {}},
            {"event_id": "EVT-2", "type": "APPROVAL_REQUESTED", "occurred_at": "2026-09-13T10:30:00Z", "data": {"approval_id": "APR-1"}},
            {"event_id": "EVT-3", "type": "SCOPE_CHANGED", "occurred_at": "2026-09-13T11:00:00Z", "data": {"requirements_added": 2, "requirements_removed": 1}},
            {"event_id": "EVT-4", "type": "SPEC_DEBT_OPENED", "occurred_at": "2026-09-13T11:30:00Z", "data": {"debt_id": "DEBT-1"}},
            {"event_id": "EVT-5", "type": "PHASE_COMPLETED", "occurred_at": "2026-09-13T12:00:00Z", "phase": "review", "version": "1.0.0", "data": {}}
        ]}
        result = METRICS.derive(payload)
        self.assertEqual(result["cycle_times_hours"]["review@1.0.0"], 2.0)
        self.assertEqual(result["scope_change"]["requirements_added"], 2)
        self.assertEqual(result["spec_debt"]["currently_open"], 1)
        self.assertEqual(result["spec_debt"]["opened"], 1)
        self.assertEqual(result["pending_approvals"][0]["approval_id"], "APR-1")
        self.assertEqual(result["pending_approvals"][0]["age_hours_at_period_end"], 1.5)

    def test_dashboard_coverage_and_risk(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.canonical_project(root)
            (root / "risks/RISK_REGISTER.md").write_text("## RISK-001 — Critique\n- Score : 25\n- Statut : OPEN\n", encoding="utf-8")
            result = DASHBOARD.compute(root)
            self.assertEqual(result["coverage"]["requirements_with_test_percent"], 100.0)
            self.assertEqual(result["risks"]["critical_open"], 1)


if __name__ == "__main__":
    unittest.main()
