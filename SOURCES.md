# Design sources

[Lire en français](SOURCES.fr.md)

Consulted on September 13, 2026.

## Normative documentation

- [Extend Claude with skills](https://code.claude.com/docs/skills) — `SKILL.md` structure, frontmatter, invocation, supporting files, context, arguments, and validation.
- [Create custom subagents](https://code.claude.com/docs/sub-agents) — locations, frontmatter, tools, limits, and plugin distribution.
- [Claude Code plugins reference](https://code.claude.com/docs/plugins-reference) — manifest, `skills/` and `agents/` tree, skills-directory plugins, and MCP restrictions for plugin agents.
- [Test plugins with evals](https://code.claude.com/docs/plugin-evals) — case structure, graders, baseline, costs, and minimum version.
- [Connect Claude Code to tools via MCP](https://code.claude.com/docs/mcp) — configuration, scope, and permissions of MCP servers.
- [Agent Skills](https://agentskills.io) — open standard followed by Claude Code skills.

## Source bundled with the project

- `sources/official-documentation.txt` — text copy of the official documentation bundled with the project.

## Compliance choices applied

- `SKILL.md` has frontmatter on the first line and a kebab-case name.
- The body of `SKILL.md` stays under the recommended 500-line limit and routes to supporting files.
- Agents are placed in `agents/` at the plugin root, with `name` and `description`.
- No plugin agent declares `mcpServers`, `hooks`, or `permissionMode`, fields unsupported at this scope.
- No fictitious MCP server is provided. The policy detects and uses only tools that are actually configured.
- Content retrieved via MCP is treated as untrusted to limit the risk of external instruction injection flagged by the official documentation.
- The plugin contains a `.claude-plugin/plugin.json` manifest and components in their default locations.
- The twenty-five V2 to V5 cases use `prompt.md` and separate graders following the official format; their execution is intentionally kept separate from package creation because it calls real models.
- The V4 baseline and redline tools use only the Python standard library. A SHA-256 hash checks integrity there without being presented as an identity signature.
- The V5 validator locally checks that every grader has the required frontmatter before distribution.
