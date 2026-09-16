# Claude Code compatibility

[Lire en français](COMPATIBILITY.fr.md)

## Versions

| Feature | Minimum documented version | V5 check |
|---|---:|---|
| Plugin and skill loading | recent supported version | Claude Code 2.1.270: PASS |
| `claude plugin validate` | 2.1.233+ | Claude Code 2.1.270: PASS |
| `claude plugin eval` | 2.1.269+ | command available; model calls not executed |

## Local dependencies

- Python 3 for validators and deterministic reports;
- Python standard library only;
- no imposed MCP server, secret, or provider;
- agents use only the frontmatter fields supported for a plugin.

## Maintenance policy

Before a release, check the official Claude Code documentation, run `claude plugin validate`, the unit suite, `validate_evals.py`, and `security_audit.py`. Any observed incompatibility must be documented before manifests or agents are modified.
