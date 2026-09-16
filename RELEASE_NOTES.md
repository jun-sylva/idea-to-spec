# Release notes

[Lire en français](RELEASE_NOTES.fr.md)

## 5.0.1 — 2026-09-14

### Documentation

- added an orchestrator–experts architecture diagram to the French and English READMEs;
- added a diagram of the approval, change, baseline, and handoff lifecycle;
- added a traceability diagram linking objectives, evidence, decisions, requirements, risks, tasks, and tests;
- added related explanations to make the plugin's behavior easier to understand.

## 5.0.0 — 2026-09-13

### Finalized

- published the final V5 package;
- added a complete English README and a complete French README;
- attributed the plugin and license to SIELINOU GAMENI Sylvain Junior;
- harmonized distribution metadata and documentation;
- fully retained the policies, 19 agents, templates, schemas, tools, and 25 evaluation cases from the release candidate.

### Validation

- all free local checks run before packaging;
- the paid behavioral benchmark remains explicitly deferred and no measured performance is claimed.

## 5.0.0-rc.1 — 2026-09-13

### Added

- reproducible testing, localization, and untrusted-content hardening policies;
- pre-registered benchmark manifest with release thresholds;
- normalized format and baseline/plugin results aggregator;
- local evaluation format validator;
- local audit of secrets, sensitive files, symbolic links, and agent fields;
- ten additional scenarios, bringing the suite to 25 cases in French, English, and Spanish;
- adversarial cases for MCP injection and unsourced legal claims;
- migration documentation from V1 to V5, compatibility, security, and release checklist.

### Fixed

- added the official frontmatter that was missing from the eight graders introduced in V4;
- non-regression test that now prevents distributing a grader without valid metadata;
- rejection of absolute paths, traversals, and symbolic links in baseline and handoff manifests.

### Status

- free checks executed;
- no model call or credit consumed;
- release candidate maintained until the behavioral benchmark and final human review.

## 4.0.0 — 2026-09-13

### Added

- configurable governance with roles, RACI, gates, quorum, and an attributable approval ledger;
- verifiable SHA-256 baselines and optional external signature references;
- archiving, retention, and redline policies;
- derived coverage and risk dashboards;
- handoff package with gate and acknowledgment of receipt;
- append-only event log and lifecycle metrics;
- local tools for baseline management, version comparison, dashboards, and metrics;
- `governance-reviewer` and `handoff-reviewer` agents;
- four V4 evaluation cases, bringing the total to fifteen.

### Guarantees

- no identity, approval, or signature is invented;
- an integrity hash is never treated as a signature;
- a modified baseline or a missing receipt blocks the gate;
- model-based evaluations remain deferred until credits are available.

## 3.0.0 — 2026-09-13

### Added

- two-gate MCP workflow: approved plan, then verified execution;
- conceptual adapters for GitHub Issues, Jira, Linear, and Notion;
- JSON synchronization plans and logs;
- import with mapping and provenance preservation;
- machine-readable provenance and JSON schemas;
- deterministic drift detection;
- transitive impact analysis for Change Requests;
- research orchestration under budget and stop conditions;
- multi-jurisdiction management;
- `integration-planner`, `change-impact-analyst`, and `jurisdiction-coordinator` agents;
- four V3 evaluation cases, bringing the total to eleven.

### Security

- no fictitious MCP integration or configuration is provided;
- MCP content is treated as untrusted;
- deletions remain separate and explicitly authorized;
- every write is reviewed and logged without a secret.

### Validation

- eleven local tests cover the validator, drift, and impact analysis;
- model-based evaluations remain deferred until credits are available.

## 2.0.0 — 2026-09-13

### Added

- `lean`, `standard`, and `regulated` profiles with validated selection;
- extensions for software, service, internal process, and hybrid product;
- `data-ai-expert` and `accessibility-expert` agents;
- protocol and template for the agent conflict register;
- specification validator with no external dependency;
- five automated validator tests;
- seven evaluation cases in the official Claude Code Plugin Evals format.

### Changed

- agent routing adapted to the profile;
- memory, project, and specification enriched with profile and type;
- deterministic check requested before final validation when Python 3 is available;
- installation and sources documentation updated.

### Known limitation

The behavioral suite was not run in the creation environment: Claude Code 2.1.153 is installed there, while `claude plugin eval` requires 2.1.269 or later and performs real model calls.

## 1.0.0 — 2026-09-13

- First version of the Idea to Spec workflow, its twelve agents, policies, and eight canonical templates.
