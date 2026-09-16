#!/usr/bin/env python3
"""Build a traceability impact graph from Idea to Spec documents."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict, deque
from pathlib import Path


ID = re.compile(r"\b(?:FR|NFR|SEC|US|TASK|TEST|DEC|RISK|OQ|ASM|OBJ|CON|CR|EVID|CONFLICT|JUR)-[A-Za-z0-9][A-Za-z0-9.-]*\b")


def markdown_files(root: Path) -> list[Path]:
    ignored = {".git", "node_modules", "evals", "templates"}
    return sorted(path for path in root.rglob("*.md") if not any(part in ignored for part in path.parts))


def analysis_units(text: str) -> list[tuple[int, str]]:
    units: list[tuple[int, str]] = []
    for match in re.finditer(r"\S(?:.*?)(?=\n\s*\n|\Z)", text, re.DOTALL):
        units.append((text.count("\n", 0, match.start()) + 1, match.group(0)))

    headings = list(re.finditer(r"^(#{1,6})\s+.+$", text, re.MULTILINE))
    for index, heading in enumerate(headings):
        level = len(heading.group(1))
        end = len(text)
        for candidate in headings[index + 1:]:
            if len(candidate.group(1)) <= level:
                end = candidate.start()
                break
        units.append((text.count("\n", 0, heading.start()) + 1, text[heading.start():end]))
    return units


def build_graph(root: Path) -> tuple[dict[str, set[str]], dict[tuple[str, str], list[dict[str, object]]]]:
    graph: dict[str, set[str]] = defaultdict(set)
    evidence: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for path in markdown_files(root):
        text = path.read_text(encoding="utf-8")
        for line, block in analysis_units(text):
            identifiers = sorted(set(ID.findall(block)))
            for identifier in identifiers:
                graph.setdefault(identifier, set())
            for index, left in enumerate(identifiers):
                for right in identifiers[index + 1:]:
                    graph[left].add(right)
                    graph[right].add(left)
                    key = tuple(sorted((left, right)))
                    reference = {"path": str(path.relative_to(root)), "line": line}
                    if reference not in evidence[key]:
                        evidence[key].append(reference)
    return graph, evidence


def traverse(graph: dict[str, set[str]], seeds: list[str], depth: int) -> dict[str, int]:
    distances = {seed: 0 for seed in seeds}
    queue = deque(seeds)
    while queue:
        current = queue.popleft()
        if distances[current] >= depth:
            continue
        for neighbor in sorted(graph[current]):
            if neighbor not in distances:
                distances[neighbor] = distances[current] + 1
                queue.append(neighbor)
    return distances


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--ids", nargs="+", required=True)
    parser.add_argument("--depth", type=int, default=3)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)

    root = args.project.expanduser().resolve()
    if not root.is_dir() or args.depth < 0:
        print("ERROR: dossier invalide ou profondeur négative.")
        return 1
    try:
        graph, evidence = build_graph(root)
    except (OSError, UnicodeDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 1

    seeds = list(dict.fromkeys(args.ids))
    unknown = [seed for seed in seeds if seed not in graph]
    if unknown:
        print(f"ERROR: identifiant(s) inconnu(s) : {', '.join(unknown)}")
        return 1

    distances = traverse(graph, seeds, args.depth)
    impacted = []
    for identifier, distance in sorted(distances.items(), key=lambda item: (item[1], item[0])):
        links = []
        for neighbor in sorted(graph[identifier]):
            if neighbor in distances and distances[neighbor] <= distance:
                links.extend(evidence.get(tuple(sorted((identifier, neighbor))), []))
        impacted.append({"id": identifier, "distance": distance, "evidence": links[:5]})

    payload = {"seeds": seeds, "max_depth": args.depth, "impacted_count": len(impacted), "impacted": impacted}
    if args.as_json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"Impact graph: {len(impacted)} identifiant(s), profondeur {args.depth}")
        for item in impacted:
            marker = "SEED" if item["distance"] == 0 else f"D{item['distance']}"
            locations = ", ".join(f"{ref['path']}:{ref['line']}" for ref in item["evidence"]) or "relation implicite à vérifier"
            print(f"{marker} {item['id']} — {locations}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
