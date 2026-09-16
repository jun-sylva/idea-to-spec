# Installation and usage

[Lire en français](INSTALLATION.fr.md)

> Idea to Spec `5.0.1` — SIELINOU GAMENI Sylvain Junior. Full documentation: [English](README.md) · [français](README.fr.md).

## Recommended option — full local plugin

This option loads the skill and the nineteen specialized agents.

1. Unzip the `idea-to-spec` folder.
2. For a one-off trial, launch Claude Code with:

   ```bash
   claude --plugin-dir /absolute/path/to/idea-to-spec
   ```

3. Invoke the skill with:

   ```text
   /idea-to-spec:idea-to-spec My project idea…
   ```

To make it available as a personal skills-directory plugin, place the complete folder in `~/.claude/skills/idea-to-spec/`, then start a new Claude Code session. The `.claude-plugin/plugin.json` manifest lets Claude Code load it as `idea-to-spec@skills-dir` with its agents.

After modifying the agents or the manifest, run `/reload-plugins` or restart Claude Code. Changes to `SKILL.md` are detected directly in recent versions.

## Minimal option — skill only

Copy `skills/idea-to-spec/` to `.claude/skills/idea-to-spec/` in a project, or to `~/.claude/skills/idea-to-spec/` for all projects. The workflow remains usable, but the plugin's custom agents will not be registered; the skill will then apply their protocols itself when needed.

## Recommended first trial

```text
/idea-to-spec:idea-to-spec I want to build an app that helps [audience] achieve [outcome].
```

The skill should read any existing memory, ask only the critical questions, present the scope, and then stop to obtain intermediate approval. It must not produce the complete specification in the same turn without that approval.

## Technical validation

With Claude Code v2.1.233 or later:

```bash
claude plugin validate /absolute/path/to/idea-to-spec
```

The package includes no MCP server or secret. It uses web or MCP capabilities only when they are actually available in the session.

## V2 to V5 validator

Check a specification folder before final validation:

```bash
python3 /path/to/idea-to-spec/skills/idea-to-spec/scripts/validate_spec.py /path/to/the-project
```

Add `--json` for a structured report or `--strict` to fail the command on warnings.

## V2 to V5 evaluations

The `evals/` folder follows the official `claude plugin eval` format. Running it requires Claude Code v2.1.269 or later and performs real model calls:

```bash
cd /path/to/idea-to-spec
claude plugin eval . --no-publish --max-cost-usd 10
```

You may want to start with a single case and a single run to limit cost. Do not treat this exploratory pass as a stable measurement.

## V5 validation without credits

These commands make no model calls:

```bash
python3 /path/to/scripts/validate_evals.py /path/to/idea-to-spec/evals
python3 /path/to/scripts/security_audit.py /path/to/idea-to-spec
python3 -m unittest discover -s /path/to/scripts/tests -p 'test_*.py'
```

The full campaign is described in `evals/BENCHMARK.md`. With 25 cases, two variants, and three repetitions, it plans for 150 runs. Display and get the cost cap approved before launching it.

After normalizing the results:

```bash
python3 /path/to/scripts/benchmark_report.py \
  /path/to/idea-to-spec/evals/BENCHMARK_MANIFEST.json \
  /path/to/normalized-results.json
```

## V3 tools

Detect drift from a normalized external snapshot:

```bash
python3 /path/to/idea-to-spec/skills/idea-to-spec/scripts/detect_drift.py \
  /path/to/the-project /path/to/snapshot.json --json
```

Explore impacts related to a Change Request:

```bash
python3 /path/to/idea-to-spec/skills/idea-to-spec/scripts/analyze_impact.py \
  /path/to/the-project --ids FR-001 TASK-01-A --json
```

These scripts are local and read-only. They do not connect to external services and do not replace the orchestrator's analysis.

## V4 tools

Create a baseline after approval, then verify its integrity:

```bash
python3 /path/to/scripts/baseline_manager.py create /path/to/the-project \
  --version 1.0.0 --project-name "My project" \
  --created-at 2026-09-13T12:00:00Z --approval APR-001 \
  --output /path/to/the-project/governance/baselines/BASELINE-1.0.0.json
python3 /path/to/scripts/baseline_manager.py verify /path/to/the-project \
  /path/to/the-project/governance/baselines/BASELINE-1.0.0.json
```

Compare two versions, compute dashboards, and derive metrics:

```bash
python3 /path/to/scripts/compare_versions.py /archive/1.0.0 /archive/1.1.0
python3 /path/to/scripts/project_dashboard.py /path/to/the-project
python3 /path/to/scripts/workflow_metrics.py /path/to/the-project/governance/WORKFLOW_EVENTS.json
```

Baseline creation only writes to the requested path and refuses to overwrite an existing manifest. The other three operations are read-only.
