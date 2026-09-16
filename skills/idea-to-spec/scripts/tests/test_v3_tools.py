#!/usr/bin/env python3
"""Tests for V3 drift and impact tools."""

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
DRIFT = load("detect_drift", SCRIPTS / "detect_drift.py")
IMPACT = load("analyze_impact", SCRIPTS / "analyze_impact.py")


class V3ToolsTests(unittest.TestCase):
    def write_tasks(self, root: Path) -> None:
        path = root / "planning/TASKS.md"
        path.parent.mkdir(parents=True)
        path.write_text("""# Tâches

## US-01 — Exporter

Liée à FR-001.

### TASK-01-A — Créer l'export

Couvre US-01 et FR-001. Validée par TEST-01.
""", encoding="utf-8")

    def snapshot(self, path: Path, items: list[dict]) -> None:
        path.write_text(json.dumps({
            "schema_version": "1.0",
            "system": "test",
            "workspace": "demo",
            "observed_at": "2026-09-13T00:00:00Z",
            "items": items,
        }), encoding="utf-8")

    def quiet(self, function, args: list[str]) -> int:
        with redirect_stdout(io.StringIO()):
            return function(args)

    def test_drift_free_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.write_tasks(root)
            canonical = DRIFT.canonical_items(root / "planning/TASKS.md")
            snapshot = root / "snapshot.json"
            self.snapshot(snapshot, [
                {"external_id": "1", "canonical_id": key, "title": value["title"], "state": "open", "content_hash": value["content_hash"]}
                for key, value in canonical.items()
            ])
            self.assertEqual(self.quiet(DRIFT.main, [str(root), str(snapshot)]), 0)

    def test_drift_detects_title_missing_and_unknown(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.write_tasks(root)
            snapshot = root / "snapshot.json"
            self.snapshot(snapshot, [
                {"external_id": "1", "canonical_id": "US-01", "title": "Titre modifié", "state": "open"},
                {"external_id": "2", "canonical_id": None, "title": "Inconnu", "state": "open"},
            ])
            self.assertEqual(self.quiet(DRIFT.main, [str(root), str(snapshot)]), 2)

    def test_impact_follows_transitive_links(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.write_tasks(root)
            requirements = root / "requirements/REQUIREMENTS.md"
            requirements.parent.mkdir(parents=True)
            requirements.write_text("# Exigences\n\n### FR-001 — Export\n\nCouvert par US-01.\n", encoding="utf-8")
            output = io.StringIO()
            with redirect_stdout(output):
                result = IMPACT.main([str(root), "--ids", "FR-001", "--json"])
            payload = json.loads(output.getvalue())
            identifiers = {item["id"] for item in payload["impacted"]}
            self.assertEqual(result, 0)
            self.assertTrue({"FR-001", "US-01", "TASK-01-A", "TEST-01"}.issubset(identifiers))

    def test_impact_rejects_unknown_seed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.write_tasks(root)
            self.assertEqual(self.quiet(IMPACT.main, [str(root), "--ids", "FR-999"]), 1)


if __name__ == "__main__":
    unittest.main()
