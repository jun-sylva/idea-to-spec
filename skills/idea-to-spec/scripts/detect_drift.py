#!/usr/bin/env python3
"""Compare canonical work items with a normalized external snapshot."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


HEADING = re.compile(r"^(#{2,6})\s+((?:US|TASK)-[A-Za-z0-9][A-Za-z0-9.-]*)\s*(?:[—:-]\s*)?(.+?)\s*$", re.MULTILINE)


@dataclass(frozen=True)
class Drift:
    kind: str
    canonical_id: str | None
    external_id: str | None
    detail: str


def block_hash(value: str) -> str:
    normalized = "\n".join(line.rstrip() for line in value.strip().splitlines())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def canonical_items(tasks_path: Path) -> dict[str, dict[str, str]]:
    text = tasks_path.read_text(encoding="utf-8")
    matches = list(HEADING.finditer(text))
    result: dict[str, dict[str, str]] = {}
    for index, match in enumerate(matches):
        identifier = match.group(2)
        if identifier in result:
            raise ValueError(f"Identifiant canonique dupliqué : {identifier}")
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        block = text[match.start():end]
        result[identifier] = {"title": match.group(3).strip(), "content_hash": block_hash(block)}
    return result


def load_snapshot(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    required = {"schema_version", "system", "workspace", "observed_at", "items"}
    missing = sorted(required - set(data)) if isinstance(data, dict) else sorted(required)
    if missing:
        raise ValueError(f"Champs snapshot manquants : {', '.join(missing)}")
    if data["schema_version"] != "1.0" or not isinstance(data["items"], list):
        raise ValueError("Le snapshot doit utiliser schema_version 1.0 et contenir une liste items.")
    item_fields = {"external_id", "canonical_id", "title", "state"}
    for index, item in enumerate(data["items"]):
        if not isinstance(item, dict):
            raise ValueError(f"L'élément externe {index} doit être un objet.")
        missing_item_fields = sorted(item_fields - set(item))
        if missing_item_fields:
            raise ValueError(f"L'élément externe {index} manque : {', '.join(missing_item_fields)}")
    return data


def compare(canonical: dict[str, dict[str, str]], snapshot: dict, source_version: str | None) -> list[Drift]:
    drift: list[Drift] = []
    mapped: dict[str, list[dict]] = {}
    for item in snapshot["items"]:
        if not isinstance(item, dict) or not item.get("external_id"):
            raise ValueError("Chaque élément externe doit contenir external_id.")
        canonical_id = item.get("canonical_id")
        if not canonical_id:
            drift.append(Drift("UNKNOWN_EXTERNAL", None, item["external_id"], "Aucun identifiant canonique."))
            continue
        mapped.setdefault(canonical_id, []).append(item)

    for canonical_id, items in mapped.items():
        if len(items) > 1:
            drift.append(Drift("MAPPING_CONFLICT", canonical_id, None, f"{len(items)} objets externes portent le même identifiant canonique."))
        if canonical_id not in canonical:
            for item in items:
                drift.append(Drift("UNKNOWN_EXTERNAL", canonical_id, item["external_id"], "Identifiant absent du plan canonique."))
            continue
        local = canonical[canonical_id]
        for item in items:
            external_id = item["external_id"]
            if str(item.get("title", "")).strip() != local["title"]:
                drift.append(Drift("TITLE_CHANGED", canonical_id, external_id, f"Canonique={local['title']!r}; externe={item.get('title', '')!r}."))
            if item.get("content_hash") and item["content_hash"] != local["content_hash"]:
                drift.append(Drift("CONTENT_CHANGED", canonical_id, external_id, "L'empreinte du contenu diffère."))
            if source_version and item.get("source_version") and item["source_version"] != source_version:
                drift.append(Drift("STALE_SOURCE_VERSION", canonical_id, external_id, f"Attendu {source_version}, observé {item['source_version']}."))

    for canonical_id in sorted(set(canonical) - set(mapped)):
        drift.append(Drift("MISSING_EXTERNAL", canonical_id, None, "Aucun objet externe correspondant."))
    return drift


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("--source-version")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)

    try:
        canonical = canonical_items(args.project.expanduser().resolve() / "planning/TASKS.md")
        snapshot = load_snapshot(args.snapshot.expanduser().resolve())
        items = compare(canonical, snapshot, args.source_version)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"valid": False, "error": str(exc)}, ensure_ascii=False) if args.as_json else f"ERROR: {exc}")
        return 1

    counts: dict[str, int] = {}
    for item in items:
        counts[item.kind] = counts.get(item.kind, 0) + 1
    payload = {
        "valid": True,
        "system": snapshot["system"],
        "workspace": snapshot["workspace"],
        "observed_at": snapshot["observed_at"],
        "canonical_count": len(canonical),
        "external_count": len(snapshot["items"]),
        "drift_count": len(items),
        "summary": counts,
        "drift": [asdict(item) for item in items],
    }
    if args.as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"Drift check: {len(items)} écart(s), {len(canonical)} élément(s) canoniques, {len(snapshot['items'])} externe(s)")
        for item in items:
            identity = item.canonical_id or item.external_id or "?"
            print(f"{item.kind} {identity}: {item.detail}")
    return 2 if items else 0


if __name__ == "__main__":
    sys.exit(main())
