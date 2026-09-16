#!/usr/bin/env python3
"""Compute traceability coverage and risk counters from canonical Markdown."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQ = re.compile(r"^#{2,6}\s+((?:FR|NFR|SEC)-[A-Za-z0-9.-]+)\b", re.MULTILINE)
TASK = re.compile(r"^#{2,6}\s+(TASK-[A-Za-z0-9.-]+)\b", re.MULTILINE)
TEST = re.compile(r"\bTEST-[A-Za-z0-9.-]+\b")
RISK_HEADER = re.compile(r"^#{2,6}\s+(RISK-[A-Za-z0-9.-]+)\b", re.MULTILINE)


def blocks(text: str, pattern: re.Pattern[str]) -> dict[str, str]:
    matches = list(pattern.finditer(text))
    return {match.group(1): text[match.start():(matches[index + 1].start() if index + 1 < len(matches) else len(text))] for index, match in enumerate(matches)}


def percent(value: int, total: int) -> float | None:
    return round(value * 100 / total, 1) if total else None


def compute(root: Path) -> dict:
    req_text = (root / "requirements/REQUIREMENTS.md").read_text(encoding="utf-8")
    task_text = (root / "planning/TASKS.md").read_text(encoding="utf-8")
    risk_path = root / "risks/RISK_REGISTER.md"
    risk_text = risk_path.read_text(encoding="utf-8") if risk_path.is_file() else ""
    requirements = sorted(set(REQ.findall(req_text)))
    task_sections = blocks(task_text, TASK)
    with_task = [rid for rid in requirements if any(re.search(rf"\b{re.escape(rid)}\b", block) for block in task_sections.values())]
    with_test = [rid for rid in requirements if any(re.search(rf"\b{re.escape(rid)}\b", block) and TEST.search(block) for block in task_sections.values())]
    linked_tasks = [tid for tid, block in task_sections.items() if REQ.search(block) or re.search(r"\bRISK-[A-Za-z0-9.-]+\b", block)]
    risk_counts = {"OPEN": 0, "MITIGATED": 0, "ACCEPTED": 0, "CLOSED": 0, "critical_open": 0, "accepted_without_decision": 0}
    for block in blocks(risk_text, RISK_HEADER).values():
        status_match = re.search(r"^- Statut\s*:\s*(OPEN|MITIGATED|ACCEPTED|CLOSED)\b", block, re.MULTILINE)
        score_match = re.search(r"^- Score\s*:\s*(\d+)", block, re.MULTILINE)
        status = status_match.group(1) if status_match else "OPEN"
        risk_counts[status] += 1
        if status == "OPEN" and score_match and int(score_match.group(1)) >= 20:
            risk_counts["critical_open"] += 1
        if status == "ACCEPTED" and not re.search(r"\bDEC-[A-Za-z0-9.-]+\b", block):
            risk_counts["accepted_without_decision"] += 1
    return {"coverage": {"requirements_total": len(requirements), "requirements_with_task": len(with_task), "requirements_with_task_percent": percent(len(with_task), len(requirements)), "requirements_with_test": len(with_test), "requirements_with_test_percent": percent(len(with_test), len(requirements)), "tasks_total": len(task_sections), "tasks_linked": len(linked_tasks), "tasks_linked_percent": percent(len(linked_tasks), len(task_sections)), "requirements_without_task": sorted(set(requirements) - set(with_task)), "requirements_without_test": sorted(set(requirements) - set(with_test)), "orphan_tasks": sorted(set(task_sections) - set(linked_tasks))}, "risks": risk_counts}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    args = parser.parse_args(argv)
    try:
        result = compute(args.project.expanduser().resolve())
    except (OSError, UnicodeDecodeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
