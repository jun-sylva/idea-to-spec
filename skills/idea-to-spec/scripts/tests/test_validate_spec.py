#!/usr/bin/env python3
"""Unit tests for validate_spec.py."""

from __future__ import annotations

import importlib.util
import io
import hashlib
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "validate_spec.py"
SPEC = importlib.util.spec_from_file_location("validate_spec", SCRIPT)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)


class ValidatorTests(unittest.TestCase):
    def make_project(self, root: Path, *, status: str = "REVIEW", profile: str = "standard") -> None:
        files = {
            "MEMORY.md": "# Mémoire\n",
            "PROJECT.md": "# Projet\n\n## Questions ouvertes\n\n| ID | Question | Impact | Responsable | Bloquante |\n|---|---|---|---|---|\n",
            "requirements/REQUIREMENTS.md": f"""# Cahier des charges

- Version : 1.0.0
- Statut : {status}
- Profil : {profile}
- Approbation utilisateur : oui

## Exigences fonctionnelles
### FR-001 — Fonction

## Exigences non fonctionnelles
### NFR-001 — Performance

## Sécurité
### SEC-001 — Accès

## Definition of Ready
- [x] Complet

## Validation finale
- Statut : APPROVED
""",
            "planning/TASKS.md": """# Tâches
### TASK-01-A — Fonction
- Exigences couvertes : FR-001 NFR-001 SEC-001
""",
            "decisions/DECISIONS.md": "# Décisions\n",
            "risks/RISK_REGISTER.md": "# Risques\n",
            "CHANGELOG.md": "# Historique\n",
        }
        if profile == "regulated":
            files["research/RESEARCH.md"] = "# Recherche\n"
            files["research/PROVENANCE.json"] = '{"schema_version":"1.0","project":"test","updated_at":"2026-09-13","entries":[]}'
        for relative, content in files.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    def run_validator(self, root: Path) -> int:
        with redirect_stdout(io.StringIO()):
            return VALIDATOR.main([str(root)])

    def add_valid_v4_governance(self, root: Path) -> None:
        governance = root / "governance"
        governance.mkdir(parents=True, exist_ok=True)
        (governance / "GOVERNANCE.md").write_text("# Gouvernance\n", encoding="utf-8")
        (governance / "RACI.md").write_text("| Livrable / décision | Produit | User approver |\n|---|---|---|\n| Cahier | R | A |\n", encoding="utf-8")
        (governance / "APPROVAL_LEDGER.json").write_text(json.dumps({"schema_version": "1.0", "project": "test", "entries": [{"approval_id": "APR-001", "gate_id": "GATE-02", "subject": "Final", "version": "1.0.0", "baseline_id": "BASELINE-1.0.0", "role": "user-approver", "actor": "Client", "decision": "APPROVED", "decided_at": "2026-09-13T12:00:00Z", "evidence_ref": "session:1", "supersedes": None}]}), encoding="utf-8")
        (governance / "APPROVAL_POLICY.json").write_text(json.dumps({"schema_version": "1.0", "project": "test", "gates": [{"gate_id": "GATE-02", "purpose": "FINAL_SPEC", "version": "1.0.0", "required_roles": ["user-approver"], "rule": "SINGLE", "quorum": 1, "status": "ACTIVE"}]}), encoding="utf-8")
        files = []
        for relative in VALIDATOR.CANONICAL_FILES:
            data = (root / relative).read_bytes()
            files.append({"path": relative, "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)})
        baseline_dir = governance / "baselines"
        baseline_dir.mkdir()
        (baseline_dir / "BASELINE-1.0.0.json").write_text(json.dumps({"schema_version": "1.0", "baseline_id": "BASELINE-1.0.0", "project": "test", "version": "1.0.0", "created_at": "2026-09-13T12:01:00Z", "status": "BASELINED", "approval_refs": ["APR-001"], "signature_status": "NOT_SIGNED", "signature_ref": None, "files": files}), encoding="utf-8")

    def test_valid_standard_project_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_project(root)
            self.assertEqual(self.run_validator(root), 0)

    def test_valid_ready_v4_project_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_project(root, status="READY_FOR_IMPLEMENTATION")
            self.add_valid_v4_governance(root)
            self.assertEqual(self.run_validator(root), 0)

    def test_missing_documents_fail(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            self.assertEqual(self.run_validator(Path(temp)), 1)

    def test_duplicate_requirement_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_project(root)
            path = root / "requirements/REQUIREMENTS.md"
            path.write_text(path.read_text(encoding="utf-8") + "\n### FR-001 — Doublon\n", encoding="utf-8")
            self.assertEqual(self.run_validator(root), 1)

    def test_ready_with_unchecked_gate_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_project(root, status="READY_FOR_IMPLEMENTATION")
            path = root / "requirements/REQUIREMENTS.md"
            text = path.read_text(encoding="utf-8").replace("- [x] Complet", "- [ ] Complet")
            path.write_text(text, encoding="utf-8")
            self.assertEqual(self.run_validator(root), 1)

    def test_regulated_requires_research(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_project(root, profile="regulated")
            (root / "research/RESEARCH.md").unlink()
            self.assertEqual(self.run_validator(root), 1)

    def test_regulated_requires_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_project(root, profile="regulated")
            (root / "research/PROVENANCE.json").unlink()
            self.assertEqual(self.run_validator(root), 1)

    def test_malformed_sync_plan_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_project(root)
            path = root / "integrations/SYNC_PLAN.json"
            path.parent.mkdir(parents=True)
            path.write_text("{not-json", encoding="utf-8")
            self.assertEqual(self.run_validator(root), 1)

    def test_unattributable_approval_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_project(root)
            path = root / "governance/APPROVAL_LEDGER.json"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps({"schema_version": "1.0", "project": "test", "entries": [{"approval_id": "APR-001", "decision": "APPROVED", "actor": "", "decided_at": None, "evidence_ref": None}]}), encoding="utf-8")
            self.assertEqual(self.run_validator(root), 1)

    def test_raci_requires_one_accountable_per_row(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_project(root)
            path = root / "governance/RACI.md"
            path.parent.mkdir(parents=True)
            path.write_text("| Livrable / décision | Produit | Technique |\n|---|---|---|\n| Cahier | A | A |\n", encoding="utf-8")
            self.assertEqual(self.run_validator(root), 1)

    def test_accepted_handoff_requires_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.make_project(root)
            path = root / "handoff/HANDOFF_MANIFEST.json"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps({"schema_version": "1.0", "status": "ACCEPTED", "files": [], "recipient_role": "dev", "baseline_id": "BASELINE-1.0.0", "receipt": None}), encoding="utf-8")
            self.assertEqual(self.run_validator(root), 1)


if __name__ == "__main__":
    unittest.main()
