#!/usr/bin/env python3
"""Run a conservative local security audit of an Idea to Spec package."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


SECRET_PATTERNS = {
    "PRIVATE_KEY": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "OPENAI_KEY": re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b"),
    "AWS_ACCESS_KEY": re.compile(r"\bAKIA[A-Z0-9]{16}\b"),
    "GITHUB_TOKEN": re.compile(r"\bgh[ps]_[A-Za-z0-9]{30,}\b"),
}
FORBIDDEN_NAMES = {".env", ".npmrc", ".pypirc", "credentials", "credentials.json", "id_rsa", "id_ed25519"}
FORBIDDEN_AGENT_FIELDS = re.compile(r"^(mcpServers|hooks|permissionMode)\s*:", re.MULTILINE)


def audit(root: Path) -> list[dict[str, str]]:
    findings = []
    for path in sorted(root.rglob("*")):
        relative = str(path.relative_to(root))
        if path.is_symlink():
            findings.append({"severity": "ERROR", "code": "SYMLINK", "path": relative})
            continue
        if not path.is_file():
            continue
        if path.name in FORBIDDEN_NAMES or path.suffix.lower() in {".pem", ".key", ".p12", ".pfx"}:
            findings.append({"severity": "ERROR", "code": "SENSITIVE_FILE", "path": relative})
        if path.name == ".DS_Store" or path.name.startswith("._") or "__pycache__" in path.parts or path.suffix == ".pyc":
            findings.append({"severity": "ERROR", "code": "BUILD_ARTIFACT", "path": relative})
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for name, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                findings.append({"severity": "ERROR", "code": name, "path": relative})
        if relative.startswith("agents/") and FORBIDDEN_AGENT_FIELDS.search(text.split("---", 2)[1] if text.startswith("---") else ""):
            findings.append({"severity": "ERROR", "code": "UNSUPPORTED_AGENT_FIELD", "path": relative})
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv)
    root = args.package.expanduser().resolve()
    findings = audit(root) if root.is_dir() else [{"severity": "ERROR", "code": "INVALID_ROOT", "path": str(root)}]
    payload = {"valid": not findings, "errors": len(findings), "findings": findings}
    print(json.dumps(payload, ensure_ascii=False, indent=2) if args.as_json else ("Security audit: PASS" if not findings else "\n".join(f"{x['severity']} {x['code']}: {x['path']}" for x in findings)))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
