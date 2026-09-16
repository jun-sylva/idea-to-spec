# Installation et usage

> Idea to Spec `5.0.1` — SIELINOU GAMENI Sylvain Junior. Documentation complète : [français](README.fr.md) · [English](README.md).

## Option recommandée — plugin local complet

Cette option charge le skill et les dix-neuf agents spécialisés.

1. Décompresser le dossier `idea-to-spec`.
2. Pour un essai ponctuel, lancer Claude Code avec :

   ```bash
   claude --plugin-dir /chemin/absolu/vers/idea-to-spec
   ```

3. Invoquer le skill avec :

   ```text
   /idea-to-spec:idea-to-spec Mon idée de projet…
   ```

Pour le rendre disponible comme plugin de répertoire de skills personnel, placer le dossier complet dans `~/.claude/skills/idea-to-spec/`, puis démarrer une nouvelle session Claude Code. Le manifeste `.claude-plugin/plugin.json` permet à Claude Code de le charger comme `idea-to-spec@skills-dir` avec ses agents.

Après une modification des agents ou du manifeste, exécuter `/reload-plugins` ou redémarrer Claude Code. Les changements de `SKILL.md` sont détectés directement dans les versions récentes.

## Option minimale — skill seul

Copier `skills/idea-to-spec/` vers `.claude/skills/idea-to-spec/` dans un projet ou vers `~/.claude/skills/idea-to-spec/` pour tous les projets. Le workflow reste utilisable, mais les agents personnalisés du plugin ne seront pas enregistrés ; le skill appliquera alors leurs protocoles lui-même lorsque nécessaire.

## Premier essai conseillé

```text
/idea-to-spec:idea-to-spec Je veux créer une application qui aide [public] à [résultat].
```

Le skill doit lire une éventuelle mémoire, poser seulement les questions critiques, présenter le cadrage puis s'arrêter pour obtenir la validation intermédiaire. Il ne doit pas produire le cahier des charges complet dans le même tour sans cette validation.

## Validation technique

Avec Claude Code v2.1.233 ou ultérieur :

```bash
claude plugin validate /chemin/absolu/vers/idea-to-spec
```

Le package n'inclut aucun serveur MCP ni secret. Il utilise les capacités web ou MCP uniquement si elles sont réellement disponibles dans la session.

## Validateur V2 à V5

Contrôler un dossier de spécification avant la validation finale :

```bash
python3 /chemin/vers/idea-to-spec/skills/idea-to-spec/scripts/validate_spec.py /chemin/vers/le-projet
```

Ajouter `--json` pour un rapport structuré ou `--strict` pour faire échouer la commande sur les avertissements.

## Évaluations V2 à V5

Le dossier `evals/` suit le format officiel `claude plugin eval`. Son exécution requiert Claude Code v2.1.269 ou ultérieur et effectue de vrais appels modèle :

```bash
cd /chemin/vers/idea-to-spec
claude plugin eval . --no-publish --max-cost-usd 10
```

Commencer éventuellement par un seul cas et une seule exécution pour limiter le coût. Ne pas considérer ce passage exploratoire comme une mesure stable.

## Validation V5 sans crédit

Ces commandes ne réalisent aucun appel modèle :

```bash
python3 /chemin/vers/scripts/validate_evals.py /chemin/vers/idea-to-spec/evals
python3 /chemin/vers/scripts/security_audit.py /chemin/vers/idea-to-spec
python3 -m unittest discover -s /chemin/vers/scripts/tests -p 'test_*.py'
```

La campagne complète est décrite dans `evals/BENCHMARK.md`. Avec 25 cas, deux variantes et trois répétitions, elle prévoit 150 exécutions. Afficher et faire approuver le plafond financier avant son lancement.

Après normalisation des résultats :

```bash
python3 /chemin/vers/scripts/benchmark_report.py \
  /chemin/vers/idea-to-spec/evals/BENCHMARK_MANIFEST.json \
  /chemin/vers/resultats-normalises.json
```

## Outils V3

Détecter les écarts à partir d'un instantané externe normalisé :

```bash
python3 /chemin/vers/idea-to-spec/skills/idea-to-spec/scripts/detect_drift.py \
  /chemin/vers/le-projet /chemin/vers/snapshot.json --json
```

Explorer les impacts liés à une Change Request :

```bash
python3 /chemin/vers/idea-to-spec/skills/idea-to-spec/scripts/analyze_impact.py \
  /chemin/vers/le-projet --ids FR-001 TASK-01-A --json
```

Ces scripts sont locaux et en lecture seule. Ils ne se connectent pas aux services externes et ne remplacent pas l'analyse de l'orchestrateur.

## Outils V4

Créer une baseline après approbation, puis vérifier son intégrité :

```bash
python3 /chemin/vers/scripts/baseline_manager.py create /chemin/du/projet \
  --version 1.0.0 --project-name "Mon projet" \
  --created-at 2026-09-13T12:00:00Z --approval APR-001 \
  --output /chemin/du/projet/governance/baselines/BASELINE-1.0.0.json
python3 /chemin/vers/scripts/baseline_manager.py verify /chemin/du/projet \
  /chemin/du/projet/governance/baselines/BASELINE-1.0.0.json
```

Comparer deux versions, calculer les tableaux et dériver les métriques :

```bash
python3 /chemin/vers/scripts/compare_versions.py /archive/1.0.0 /archive/1.1.0
python3 /chemin/vers/scripts/project_dashboard.py /chemin/du/projet
python3 /chemin/vers/scripts/workflow_metrics.py /chemin/du/projet/governance/WORKFLOW_EVENTS.json
```

La création de baseline écrit uniquement au chemin demandé et refuse d'écraser un manifeste existant. Les trois autres opérations sont en lecture seule.
