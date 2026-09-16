#!/usr/bin/env python3
"""Validate an Idea to Spec project using only the Python standard library."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path


CANONICAL_FILES = (
    "MEMORY.md",
    "PROJECT.md",
    "requirements/REQUIREMENTS.md",
    "planning/TASKS.md",
    "decisions/DECISIONS.md",
    "risks/RISK_REGISTER.md",
    "CHANGELOG.md",
)
ALLOWED_STATUSES = {
    "DRAFT",
    "REVIEW",
    "USER_CHANGES_REQUESTED",
    "PENDING_USER_APPROVAL",
    "APPROVED",
    "READY_FOR_IMPLEMENTATION",
}
ID_PATTERN = re.compile(
    r"\b(FR|NFR|SEC|US|TASK|TEST|DEC|RISK|OQ|ASM|OBJ|CON|CR|EVID|CONFLICT)-[A-Za-z0-9][A-Za-z0-9.-]*\b"
)
HEADING_ID_PATTERN = re.compile(
    r"^#{2,6}\s+((?:FR|NFR|SEC|US|TASK|TEST|DEC|RISK|OQ|ASM|OBJ|CON|CR|EVID|CONFLICT)-[A-Za-z0-9][A-Za-z0-9.-]*)\b",
    re.MULTILINE,
)


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    message: str
    path: str | None = None


class Report:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.findings: list[Finding] = []

    def add(self, severity: str, code: str, message: str, path: Path | None = None) -> None:
        relative = None
        if path is not None:
            try:
                relative = str(path.relative_to(self.root))
            except ValueError:
                relative = str(path)
        self.findings.append(Finding(severity, code, message, relative))

    @property
    def errors(self) -> int:
        return sum(item.severity == "ERROR" for item in self.findings)

    @property
    def warnings(self) -> int:
        return sum(item.severity == "WARNING" for item in self.findings)


def normalize(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value)
    return "".join(char for char in decomposed if not unicodedata.combining(char)).lower()


def read_text(path: Path, report: Report) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        report.add("ERROR", "FILE_ENCODING", "Le fichier doit être encodé en UTF-8.", path)
    except OSError as exc:
        report.add("ERROR", "FILE_READ", f"Lecture impossible : {exc}", path)
    return ""


def safe_project_file(root: Path, relative: str) -> Path | None:
    candidate = root / relative
    if Path(relative).is_absolute() or candidate.is_symlink():
        return None
    try:
        candidate.resolve().relative_to(root)
    except (OSError, ValueError):
        return None
    return candidate if candidate.is_file() else None


def metadata_value(text: str, label: str) -> str | None:
    match = re.search(rf"^\s*[-*]?\s*{re.escape(label)}\s*:\s*(.+?)\s*$", text, re.IGNORECASE | re.MULTILINE)
    return match.group(1).strip() if match else None


def section(text: str, title: str) -> str:
    title_norm = normalize(title)
    lines = text.splitlines()
    start = None
    level = None
    for index, line in enumerate(lines):
        match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if match and title_norm in normalize(match.group(2)):
            start = index + 1
            level = len(match.group(1))
            break
    if start is None or level is None:
        return ""
    collected: list[str] = []
    for line in lines[start:]:
        match = re.match(r"^(#{1,6})\s+", line)
        if match and len(match.group(1)) <= level:
            break
        collected.append(line)
    return "\n".join(collected)


def validate_documents(root: Path, report: Report) -> dict[str, str]:
    texts: dict[str, str] = {}
    for relative in CANONICAL_FILES:
        path = root / relative
        if not path.is_file():
            report.add("ERROR", "MISSING_DOCUMENT", "Document canonique manquant.", path)
            continue
        texts[relative] = read_text(path, report)
    return texts


def validate_requirements(root: Path, texts: dict[str, str], report: Report) -> tuple[str | None, str | None]:
    relative = "requirements/REQUIREMENTS.md"
    text = texts.get(relative, "")
    path = root / relative
    if not text:
        return None, None

    version = metadata_value(text, "Version")
    if not version or not re.fullmatch(r"\d+\.\d+\.\d+", version):
        report.add("ERROR", "INVALID_VERSION", "La version doit suivre le format x.y.z.", path)

    status = metadata_value(text, "Statut")
    if status not in ALLOWED_STATUSES:
        report.add("ERROR", "INVALID_STATUS", f"Statut absent ou non reconnu : {status!r}.", path)

    profile = metadata_value(text, "Profil")
    if profile not in {"lean", "standard", "regulated"}:
        report.add("WARNING", "PROFILE_MISSING", "Profil lean, standard ou regulated non renseigné.", path)

    normalized = normalize(text)
    required_sections = (
        "exigences fonctionnelles",
        "exigences non fonctionnelles",
        "securite",
        "definition of ready",
    )
    for required in required_sections:
        if required not in normalized:
            report.add("ERROR", "MISSING_SECTION", f"Section requise absente : {required}.", path)

    definitions = HEADING_ID_PATTERN.findall(text)
    duplicates = sorted({identifier for identifier in definitions if definitions.count(identifier) > 1})
    for identifier in duplicates:
        report.add("ERROR", "DUPLICATE_ID", f"Identifiant défini plusieurs fois : {identifier}.", path)

    if profile == "regulated" and not (root / "research/RESEARCH.md").is_file():
        report.add("ERROR", "REGULATED_RESEARCH_MISSING", "Le profil regulated exige research/RESEARCH.md.", path)

    return status, profile


def validate_traceability(root: Path, texts: dict[str, str], report: Report) -> None:
    requirements_text = texts.get("requirements/REQUIREMENTS.md", "")
    tasks_text = texts.get("planning/TASKS.md", "")
    tasks_path = root / "planning/TASKS.md"
    requirement_ids = [
        identifier
        for identifier in HEADING_ID_PATTERN.findall(requirements_text)
        if identifier.startswith(("FR-", "NFR-", "SEC-"))
    ]
    if not requirement_ids:
        report.add("WARNING", "NO_REQUIREMENT_ID", "Aucune exigence FR, NFR ou SEC définie dans un titre.", root / "requirements/REQUIREMENTS.md")
    for identifier in requirement_ids:
        if not re.search(rf"\b{re.escape(identifier)}\b", tasks_text):
            report.add("WARNING", "UNCOVERED_REQUIREMENT", f"Exigence absente du plan de tâches : {identifier}.", tasks_path)

    task_matches = list(re.finditer(r"^#{2,6}\s+(TASK-[A-Za-z0-9][A-Za-z0-9.-]*)\b", tasks_text, re.MULTILINE))
    for index, match in enumerate(task_matches):
        end = task_matches[index + 1].start() if index + 1 < len(task_matches) else len(tasks_text)
        block = tasks_text[match.start():end]
        links = ID_PATTERN.findall(block)
        if not any(prefix in {"FR", "NFR", "SEC", "RISK"} for prefix in links):
            report.add("WARNING", "ORPHAN_TASK", f"Tâche sans lien vers une exigence ou un risque : {match.group(1)}.", tasks_path)


def validate_readiness(root: Path, texts: dict[str, str], status: str | None, report: Report) -> None:
    requirements_text = texts.get("requirements/REQUIREMENTS.md", "")
    if status != "READY_FOR_IMPLEMENTATION":
        return

    dor = section(requirements_text, "Definition of Ready")
    unchecked = len(re.findall(r"^- \[ \]", dor, re.MULTILINE))
    if unchecked:
        report.add("ERROR", "READINESS_INCOMPLETE", f"{unchecked} contrôle(s) de readiness restent non cochés.", root / "requirements/REQUIREMENTS.md")

    approval = metadata_value(requirements_text, "Approbation utilisateur")
    final_approval = metadata_value(section(requirements_text, "Validation finale"), "Statut")
    waiting = {None, "", "en attente", "PENDING_USER_APPROVAL"}
    if approval in waiting and final_approval in waiting:
        report.add("ERROR", "APPROVAL_MISSING", "Le statut READY_FOR_IMPLEMENTATION exige une approbation utilisateur explicite.", root / "requirements/REQUIREMENTS.md")

    project_text = texts.get("PROJECT.md", "")
    if re.search(r"^\|\s*OQ-[^\n]*\|\s*oui\s*\|\s*$", project_text, re.IGNORECASE | re.MULTILINE):
        report.add("ERROR", "BLOCKING_QUESTION", "Une question ouverte est encore marquée comme bloquante.", root / "PROJECT.md")

    conflicts_path = root / "decisions/AGENT_CONFLICTS.md"
    if conflicts_path.is_file() and re.search(r"Statut\s*:\s*OPEN\b", read_text(conflicts_path, report), re.IGNORECASE):
        report.add("ERROR", "OPEN_CONFLICT", "Un désaccord entre agents reste ouvert.", conflicts_path)


def validate_research(root: Path, texts: dict[str, str], report: Report) -> None:
    joined = "\n".join(texts.values())
    research = root / "research/RESEARCH.md"
    if re.search(r"https?://", joined) and not research.is_file():
        report.add("WARNING", "RESEARCH_LOG_MISSING", "Des URL sont citées mais aucun dossier de recherche n'est présent.", research)


def load_json_artifact(path: Path, report: Report) -> dict | None:
    if not path.is_file():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        report.add("ERROR", "INVALID_JSON", f"JSON illisible : {exc}", path)
        return None
    if not isinstance(value, dict):
        report.add("ERROR", "INVALID_JSON_ROOT", "La racine JSON doit être un objet.", path)
        return None
    return value


def validate_v3_artifacts(root: Path, status: str | None, profile: str | None, report: Report) -> None:
    provenance_path = root / "research/PROVENANCE.json"
    provenance = load_json_artifact(provenance_path, report)
    if profile == "regulated" and provenance is None:
        report.add("ERROR", "REGULATED_PROVENANCE_MISSING", "Le profil regulated exige research/PROVENANCE.json.", provenance_path)
    if provenance is not None:
        entries = provenance.get("entries")
        if provenance.get("schema_version") != "1.0" or not isinstance(entries, list):
            report.add("ERROR", "INVALID_PROVENANCE", "La provenance doit utiliser schema_version 1.0 et une liste entries.", provenance_path)
        else:
            required = {"id", "claim", "source_type", "source_uri", "checked_at", "evidence_level", "confidence", "status", "linked_ids"}
            seen: set[str] = set()
            for index, entry in enumerate(entries):
                if not isinstance(entry, dict):
                    report.add("ERROR", "INVALID_PROVENANCE_ENTRY", f"Entrée {index} non valide.", provenance_path)
                    continue
                missing = sorted(required - set(entry))
                if missing:
                    report.add("ERROR", "INCOMPLETE_PROVENANCE_ENTRY", f"{entry.get('id', index)} manque : {', '.join(missing)}.", provenance_path)
                identifier = entry.get("id")
                if identifier in seen:
                    report.add("ERROR", "DUPLICATE_PROVENANCE_ID", f"Identifiant de provenance dupliqué : {identifier}.", provenance_path)
                if identifier:
                    seen.add(identifier)

    plan_path = root / "integrations/SYNC_PLAN.json"
    plan = load_json_artifact(plan_path, report)
    if plan is not None:
        plan_status = plan.get("status")
        if plan.get("schema_version") != "1.0" or not isinstance(plan.get("operations"), list):
            report.add("ERROR", "INVALID_SYNC_PLAN", "Le plan doit utiliser schema_version 1.0 et une liste operations.", plan_path)
        if plan_status == "APPROVED" and not plan.get("approved_by"):
            report.add("ERROR", "SYNC_APPROVER_MISSING", "Un plan APPROVED doit identifier son approbateur.", plan_path)
        if status == "READY_FOR_IMPLEMENTATION" and plan_status == "PENDING_USER_APPROVAL":
            report.add("ERROR", "SYNC_PLAN_PENDING", "Un plan de synchronisation est encore en attente d'approbation.", plan_path)

    ledger_path = root / "integrations/SYNC_LEDGER.json"
    ledger = load_json_artifact(ledger_path, report)
    if ledger is not None and (ledger.get("schema_version") != "1.0" or not isinstance(ledger.get("runs"), list)):
        report.add("ERROR", "INVALID_SYNC_LEDGER", "Le journal doit utiliser schema_version 1.0 et une liste runs.", ledger_path)


def validate_v4_artifacts(root: Path, status: str | None, version: str | None, profile: str | None, report: Report) -> None:
    approval_path = root / "governance/APPROVAL_LEDGER.json"
    approval = load_json_artifact(approval_path, report)
    approved_refs: set[str] = set()
    if approval is not None:
        entries = approval.get("entries")
        if approval.get("schema_version") != "1.0" or not isinstance(entries, list):
            report.add("ERROR", "INVALID_APPROVAL_LEDGER", "Le journal doit utiliser schema_version 1.0 et une liste entries.", approval_path)
        else:
            seen: set[str] = set()
            for entry in entries:
                if not isinstance(entry, dict) or not entry.get("approval_id"):
                    report.add("ERROR", "INVALID_APPROVAL_ENTRY", "Entrée d'approbation incomplète.", approval_path)
                    continue
                identifier = entry["approval_id"]
                if identifier in seen:
                    report.add("ERROR", "DUPLICATE_APPROVAL_ID", f"Approbation dupliquée : {identifier}.", approval_path)
                seen.add(identifier)
                if entry.get("decision") == "APPROVED":
                    approved_refs.add(identifier)
                    if not entry.get("decided_at") or not entry.get("evidence_ref") or not entry.get("actor"):
                        report.add("ERROR", "UNATTRIBUTABLE_APPROVAL", f"Approbation {identifier} sans identité, date ou preuve.", approval_path)

    policy_path = root / "governance/APPROVAL_POLICY.json"
    policy = load_json_artifact(policy_path, report)
    final_gate_valid = False
    if policy is not None:
        gates = policy.get("gates")
        if policy.get("schema_version") != "1.0" or not isinstance(gates, list):
            report.add("ERROR", "INVALID_APPROVAL_POLICY", "La politique doit utiliser schema_version 1.0 et une liste gates.", policy_path)
        else:
            gate_ids = [gate.get("gate_id") for gate in gates if isinstance(gate, dict)]
            if len(gate_ids) != len(set(gate_ids)):
                report.add("ERROR", "DUPLICATE_GATE_ID", "La politique contient des gates dupliqués.", policy_path)
            entries = approval.get("entries", []) if approval else []
            superseded = {entry.get("supersedes") for entry in entries if isinstance(entry, dict) and entry.get("supersedes")}
            effective = [entry for entry in entries if isinstance(entry, dict) and entry.get("approval_id") not in superseded]
            for gate in gates:
                if not isinstance(gate, dict) or gate.get("status") != "ACTIVE":
                    continue
                roles = gate.get("required_roles", [])
                rule, quorum = gate.get("rule"), gate.get("quorum")
                if not isinstance(roles, list) or not roles or not isinstance(quorum, int) or quorum < 1:
                    report.add("ERROR", "INVALID_GATE", f"Gate invalide : {gate.get('gate_id')}.", policy_path)
                    continue
                if rule in {"SINGLE", "ANY"} and quorum != 1:
                    report.add("ERROR", "INVALID_GATE_QUORUM", f"{gate.get('gate_id')} doit avoir un quorum de 1.", policy_path)
                if rule == "ALL" and quorum != len(roles):
                    report.add("ERROR", "INVALID_GATE_QUORUM", f"{gate.get('gate_id')} ALL exige un quorum égal au nombre de rôles.", policy_path)
                if rule == "N_OF_M" and quorum > len(roles):
                    report.add("ERROR", "INVALID_GATE_QUORUM", f"{gate.get('gate_id')} a un quorum supérieur au nombre de rôles.", policy_path)
                approved_roles = {entry.get("role") for entry in effective if entry.get("gate_id") == gate.get("gate_id") and entry.get("version") == gate.get("version") and entry.get("decision") == "APPROVED"}
                satisfied = len(approved_roles.intersection(roles)) >= quorum
                if gate.get("purpose") == "FINAL_SPEC" and gate.get("version") == version:
                    final_gate_valid = satisfied

    baseline = None
    baseline_path = root / f"governance/baselines/BASELINE-{version}.json" if version else root / "governance/baselines/BASELINE-unknown.json"
    if version and baseline_path.is_file():
        baseline = load_json_artifact(baseline_path, report)
    if status == "READY_FOR_IMPLEMENTATION" and approval is None:
        report.add("ERROR", "APPROVAL_LEDGER_MISSING", "READY_FOR_IMPLEMENTATION exige un journal d'approbation.", approval_path)
    if status == "READY_FOR_IMPLEMENTATION" and baseline is None:
        report.add("ERROR", "BASELINE_MISSING", "READY_FOR_IMPLEMENTATION exige la baseline de la version courante.", baseline_path)
    if status == "READY_FOR_IMPLEMENTATION" and policy is None:
        report.add("ERROR", "APPROVAL_POLICY_MISSING", "READY_FOR_IMPLEMENTATION exige une politique d'approbation.", policy_path)
    if status == "READY_FOR_IMPLEMENTATION" and policy is not None and not final_gate_valid:
        report.add("ERROR", "FINAL_GATE_UNSATISFIED", "Le gate FINAL_SPEC de la version courante n'est pas satisfait.", policy_path)
    if status == "READY_FOR_IMPLEMENTATION" and profile in {"standard", "regulated"}:
        for relative in ("governance/GOVERNANCE.md", "governance/RACI.md"):
            path = root / relative
            if not path.is_file():
                report.add("ERROR", "GOVERNANCE_DOCUMENT_MISSING", "Document de gouvernance requis pour ce profil.", path)
    if baseline is not None:
        if baseline.get("schema_version") != "1.0" or baseline.get("version") != version or not isinstance(baseline.get("files"), list):
            report.add("ERROR", "INVALID_BASELINE", "Baseline incohérente avec la version courante.", baseline_path)
        if baseline.get("signature_status") == "EXTERNALLY_SIGNED" and not baseline.get("signature_ref"):
            report.add("ERROR", "SIGNATURE_REF_MISSING", "Une signature externe doit avoir une référence.", baseline_path)
        if status == "READY_FOR_IMPLEMENTATION" and baseline.get("status") != "BASELINED":
            report.add("ERROR", "BASELINE_NOT_ACTIVE", "La baseline courante doit avoir le statut BASELINED.", baseline_path)
        listed_paths = {item.get("path") for item in baseline.get("files", []) if isinstance(item, dict)}
        missing_canonical = sorted(set(CANONICAL_FILES) - listed_paths)
        if status == "READY_FOR_IMPLEMENTATION" and missing_canonical:
            report.add("ERROR", "BASELINE_INCOMPLETE", f"Documents canoniques absents de la baseline : {', '.join(missing_canonical)}.", baseline_path)
        refs = set(baseline.get("approval_refs", []))
        if status == "READY_FOR_IMPLEMENTATION" and (not refs or not refs.issubset(approved_refs)):
            report.add("ERROR", "BASELINE_APPROVAL_INVALID", "Les approbations de la baseline sont absentes ou non valides.", baseline_path)
        for item in baseline.get("files", []):
            if not isinstance(item, dict) or not isinstance(item.get("path"), str):
                report.add("ERROR", "INVALID_BASELINE_FILE", "Entrée de fichier invalide.", baseline_path)
                continue
            target = safe_project_file(root, item["path"])
            if target is None:
                report.add("ERROR", "BASELINE_FILE_UNSAFE", f"Chemin de baseline non sûr ou manquant : {item['path']}.", baseline_path)
                continue
            data = target.read_bytes()
            if hashlib.sha256(data).hexdigest() != item.get("sha256") or len(data) != item.get("size"):
                report.add("ERROR", "BASELINE_MISMATCH", f"Empreinte différente : {item['path']}.", baseline_path)

    raci_path = root / "governance/RACI.md"
    if raci_path.is_file():
        for line in read_text(raci_path, report).splitlines():
            if line.startswith("|") and not re.match(r"^\|[-:| ]+\|$", line) and "Livrable / décision" not in line:
                cells = [cell.strip() for cell in line.strip("|").split("|")][1:]
                if sum(cell == "A" for cell in cells) != 1:
                    report.add("ERROR", "RACI_ACCOUNTABLE_COUNT", "Chaque ligne RACI doit avoir exactement un A.", raci_path)

    events_path = root / "governance/WORKFLOW_EVENTS.json"
    events = load_json_artifact(events_path, report)
    if events is not None:
        rows = events.get("events")
        if events.get("schema_version") != "1.0" or not isinstance(rows, list):
            report.add("ERROR", "INVALID_WORKFLOW_EVENTS", "Le journal doit utiliser schema_version 1.0 et une liste events.", events_path)
        else:
            ids = [row.get("event_id") for row in rows if isinstance(row, dict)]
            if len(ids) != len(set(ids)):
                report.add("ERROR", "DUPLICATE_EVENT_ID", "Le journal contient des identifiants dupliqués.", events_path)
            timestamps = [row.get("occurred_at") for row in rows if isinstance(row, dict)]
            if timestamps != sorted(timestamps):
                report.add("WARNING", "EVENTS_NOT_CHRONOLOGICAL", "Les événements ne sont pas dans l'ordre chronologique.", events_path)

    handoff_path = root / "handoff/HANDOFF_MANIFEST.json"
    handoff = load_json_artifact(handoff_path, report)
    if handoff is not None:
        if handoff.get("schema_version") != "1.0" or not isinstance(handoff.get("files"), list):
            report.add("ERROR", "INVALID_HANDOFF", "Manifeste de handoff invalide.", handoff_path)
        if handoff.get("status") in {"HANDOFF_READY", "PENDING_RECEIPT", "ACCEPTED"}:
            if status != "READY_FOR_IMPLEMENTATION":
                report.add("ERROR", "HANDOFF_BEFORE_READY", "Le handoff ne peut être prêt avant READY_FOR_IMPLEMENTATION.", handoff_path)
            if not handoff.get("recipient_role") or not handoff.get("baseline_id"):
                report.add("ERROR", "HANDOFF_RESPONSIBILITY_MISSING", "Le handoff doit identifier la baseline et le rôle destinataire.", handoff_path)
        if handoff.get("status") == "ACCEPTED" and not handoff.get("receipt"):
            report.add("ERROR", "HANDOFF_RECEIPT_MISSING", "Un handoff ACCEPTED exige un accusé de réception.", handoff_path)
        for item in handoff.get("files", []):
            if not isinstance(item, dict) or not isinstance(item.get("path"), str):
                report.add("ERROR", "INVALID_HANDOFF_FILE", "Entrée de fichier invalide.", handoff_path)
                continue
            target = safe_project_file(root, item["path"])
            if target is None:
                report.add("ERROR", "HANDOFF_FILE_UNSAFE", f"Chemin de handoff non sûr ou manquant : {item['path']}.", handoff_path)
                continue
            data = target.read_bytes()
            if hashlib.sha256(data).hexdigest() != item.get("sha256") or len(data) != item.get("size"):
                report.add("ERROR", "HANDOFF_FILE_MISMATCH", f"Empreinte de handoff différente : {item['path']}.", handoff_path)


def render_text(report: Report) -> str:
    lines = [f"Idea to Spec validation: {report.root}"]
    for finding in report.findings:
        location = f" [{finding.path}]" if finding.path else ""
        lines.append(f"{finding.severity} {finding.code}{location}: {finding.message}")
    lines.append(f"Summary: {report.errors} error(s), {report.warnings} warning(s)")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="Dossier contenant les documents Idea to Spec")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Produire un rapport JSON")
    parser.add_argument("--strict", action="store_true", help="Traiter les avertissements comme des erreurs")
    args = parser.parse_args(argv)

    root = args.project.expanduser().resolve()
    report = Report(root)
    if not root.is_dir():
        report.add("ERROR", "INVALID_ROOT", "Le chemin fourni n'est pas un dossier.", root)
    else:
        texts = validate_documents(root, report)
        status, profile = validate_requirements(root, texts, report)
        version = metadata_value(texts.get("requirements/REQUIREMENTS.md", ""), "Version")
        validate_traceability(root, texts, report)
        validate_readiness(root, texts, status, report)
        validate_research(root, texts, report)
        validate_v3_artifacts(root, status, profile, report)
        validate_v4_artifacts(root, status, version, profile, report)

    if args.as_json:
        payload = {
            "root": str(root),
            "valid": report.errors == 0 and (not args.strict or report.warnings == 0),
            "summary": {"errors": report.errors, "warnings": report.warnings},
            "findings": [asdict(item) for item in report.findings],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(render_text(report))
    return 1 if report.errors or (args.strict and report.warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
