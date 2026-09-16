#!/usr/bin/env python3
"""Create or verify an Idea to Spec baseline manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


CANONICAL = (
    "MEMORY.md", "PROJECT.md", "requirements/REQUIREMENTS.md",
    "planning/TASKS.md", "decisions/DECISIONS.md",
    "risks/RISK_REGISTER.md", "CHANGELOG.md",
)


def safe_file(root: Path, relative: str) -> Path | None:
    candidate = root / relative
    if Path(relative).is_absolute() or candidate.is_symlink():
        return None
    try:
        candidate.resolve().relative_to(root)
    except (OSError, ValueError):
        return None
    return candidate if candidate.is_file() else None


def digest(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {"path": "", "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)}


def create(args: argparse.Namespace) -> int:
    root = args.project_root.expanduser().resolve()
    missing = [relative for relative in CANONICAL if safe_file(root, relative) is None]
    if missing:
        print(json.dumps({"error": "missing_files", "files": missing}, ensure_ascii=False, indent=2))
        return 1
    files = []
    for relative in CANONICAL:
        item = digest(safe_file(root, relative))
        item["path"] = relative
        files.append(item)
    payload = {
        "schema_version": "1.0",
        "baseline_id": f"BASELINE-{args.version}",
        "project": args.project_name,
        "version": args.version,
        "created_at": args.created_at,
        "status": "BASELINED",
        "approval_refs": sorted(set(args.approval)),
        "signature_status": "NOT_SIGNED",
        "signature_ref": None,
        "files": files,
    }
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        output = args.output.expanduser().resolve()
        if output.exists():
            print(json.dumps({"error": "output_exists", "path": str(output)}, ensure_ascii=False))
            return 1
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


def verify(args: argparse.Namespace) -> int:
    root = args.project_root.expanduser().resolve()
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(json.dumps({"valid": False, "error": str(exc)}, ensure_ascii=False, indent=2))
        return 1
    findings = []
    for item in manifest.get("files", []):
        relative = item.get("path")
        path = safe_file(root, relative) if isinstance(relative, str) else None
        if path is None:
            findings.append({"path": relative, "status": "UNSAFE_OR_MISSING"})
            continue
        actual = digest(path)
        status = "MATCH" if actual["sha256"] == item.get("sha256") and actual["size"] == item.get("size") else "MISMATCH"
        findings.append({"path": relative, "status": status, "expected_sha256": item.get("sha256"), "actual_sha256": actual["sha256"]})
    valid = bool(manifest.get("files")) and all(item["status"] == "MATCH" for item in findings)
    print(json.dumps({"valid": valid, "baseline_id": manifest.get("baseline_id"), "findings": findings}, ensure_ascii=False, indent=2))
    return 0 if valid else 2


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    make = sub.add_parser("create")
    make.add_argument("project_root", type=Path)
    make.add_argument("--version", required=True)
    make.add_argument("--project-name", required=True)
    make.add_argument("--created-at", required=True, help="Date ISO 8601 fournie explicitement")
    make.add_argument("--approval", action="append", default=[])
    make.add_argument("--output", type=Path)
    make.set_defaults(function=create)
    check = sub.add_parser("verify")
    check.add_argument("project_root", type=Path)
    check.add_argument("manifest", type=Path)
    check.set_defaults(function=verify)
    args = parser.parse_args(argv)
    if args.command == "create" and not re.fullmatch(r"\d+\.\d+\.\d+", args.version):
        parser.error("--version doit suivre x.y.z")
    return args.function(args)


if __name__ == "__main__":
    sys.exit(main())
