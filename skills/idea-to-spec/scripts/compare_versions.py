#!/usr/bin/env python3
"""Compare two Idea to Spec trees and produce a deterministic redline."""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path


ID = re.compile(r"\b(?:FR|NFR|SEC|US|TASK|TEST|DEC|RISK|CR)-[A-Za-z0-9][A-Za-z0-9.-]*\b")


def readable_files(root: Path) -> dict[str, str]:
    if root.is_file():
        return {root.name: root.read_text(encoding="utf-8")}
    result = {}
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".md", ".json"}:
            result[str(path.relative_to(root))] = path.read_text(encoding="utf-8")
    return result


def compare(source: Path, target: Path) -> dict[str, object]:
    before, after = readable_files(source), readable_files(target)
    all_paths = sorted(set(before) | set(after))
    files, chunks = [], []
    for relative in all_paths:
        old, new = before.get(relative), after.get(relative)
        if old == new:
            continue
        change = "ADDED" if old is None else "REMOVED" if new is None else "MODIFIED"
        old_text, new_text = old or "", new or ""
        chunks.extend(difflib.unified_diff(old_text.splitlines(), new_text.splitlines(), fromfile=f"a/{relative}", tofile=f"b/{relative}", lineterm=""))
        files.append({"path": relative, "change": change})
    old_ids = set(ID.findall("\n".join(before.values())))
    new_ids = set(ID.findall("\n".join(after.values())))
    return {"source": str(source), "target": str(target), "files": files, "identifiers_added": sorted(new_ids - old_ids), "identifiers_removed": sorted(old_ids - new_ids), "diff": chunks}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("target", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)
    if not args.source.exists() or not args.target.exists():
        parser.error("source et cible doivent exister")
    result = compare(args.source, args.target)
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"# Redline — {args.source.name} → {args.target.name}\n")
        print(f"- Fichiers modifiés : {len(result['files'])}")
        print(f"- Identifiants ajoutés : {', '.join(result['identifiers_added']) or 'aucun'}")
        print(f"- Identifiants retirés : {', '.join(result['identifiers_removed']) or 'aucun'}\n")
        print("```diff")
        print("\n".join(result["diff"]))
        print("```")
    return 0


if __name__ == "__main__":
    sys.exit(main())
