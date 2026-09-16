# Sources de conception

Consultées le 13 septembre 2026.

## Documentation normative

- [Étendre Claude avec des skills](https://code.claude.com/docs/fr/skills) — structure `SKILL.md`, frontmatter, invocation, fichiers de support, contexte, arguments et validation.
- [Créer des sous-agents personnalisés](https://code.claude.com/docs/fr/sub-agents) — emplacements, frontmatter, outils, limites et distribution par plugin.
- [Référence des plugins Claude Code](https://code.claude.com/docs/fr/plugins-reference) — manifeste, arborescence `skills/` et `agents/`, plugins de répertoire de skills et restrictions MCP des agents de plugin.
- [Tester les plugins avec des evals](https://code.claude.com/docs/fr/plugin-evals) — structure des cas, évaluateurs, baseline, coûts et version minimale.
- [Connecter Claude Code aux outils via MCP](https://code.claude.com/docs/fr/mcp) — configuration, portée et permissions des serveurs MCP.
- [Agent Skills](https://agentskills.io) — norme ouverte suivie par les skills Claude Code.

## Source fournie avec le projet

- `sources/official-documentation.txt` — copie texte de la documentation officielle fournie avec le projet.

## Choix de conformité appliqués

- `SKILL.md` possède un frontmatter à la première ligne et un nom en kebab-case.
- Le corps de `SKILL.md` reste sous la limite conseillée de 500 lignes et route vers des fichiers de support.
- Les agents sont placés dans `agents/` à la racine du plugin, avec `name` et `description`.
- Aucun agent de plugin ne déclare `mcpServers`, `hooks` ou `permissionMode`, champs non pris en charge pour cette portée.
- Aucun serveur MCP fictif n'est fourni. La politique détecte et utilise uniquement les outils réellement configurés.
- Les contenus récupérés via MCP sont traités comme non fiables afin de limiter les risques d'injection d'instructions externes signalés par la documentation officielle.
- Le plugin contient un manifeste `.claude-plugin/plugin.json` et les composants aux emplacements par défaut.
- Les vingt-cinq cas V2 à V5 utilisent `prompt.md` et des graders séparés selon le format officiel ; leur exécution reste volontairement séparée de la création du package car elle appelle des modèles réels.
- Les outils V4 de baseline et de redline utilisent uniquement la bibliothèque standard Python. Une empreinte SHA-256 y contrôle l'intégrité sans être présentée comme une signature d'identité.
- Le validateur V5 contrôle localement que chaque grader possède le frontmatter requis avant distribution.
