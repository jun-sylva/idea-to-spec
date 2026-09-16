# Notes de version

## 5.0.1 — 2026-09-14

### Documentation

- ajout dans les README français et anglais d'un diagramme de l'architecture orchestrateur–experts ;
- ajout d'un diagramme du cycle de validation, changement, baseline et handoff ;
- ajout d'un diagramme de traçabilité entre objectifs, preuves, décisions, exigences, risques, tâches et tests ;
- ajout d'explications associées pour rendre le fonctionnement du plugin plus facile à comprendre.

## 5.0.0 — 2026-09-13

### Finalisé

- publication du package final V5 ;
- ajout d'un README anglais complet et d'un README français complet ;
- attribution du plugin et de la licence à SIELINOU GAMENI Sylvain Junior ;
- harmonisation des métadonnées et de la documentation de distribution ;
- conservation intégrale des politiques, 19 agents, modèles, schémas, outils et 25 cas d'évaluation de la release candidate.

### Validation

- tous les contrôles locaux gratuits sont exécutés avant empaquetage ;
- le benchmark comportemental payant reste explicitement différé et aucune performance mesurée n'est revendiquée.

## 5.0.0-rc.1 — 2026-09-13

### Ajouté

- politiques de test reproductible, localisation et durcissement des contenus non fiables ;
- manifeste de benchmark préenregistré avec seuils de release ;
- format normalisé et agrégateur de résultats baseline/plugin ;
- validateur local du format des évaluations ;
- audit local des secrets, fichiers sensibles, liens symboliques et champs d'agents ;
- dix scénarios supplémentaires, portant la suite à 25 cas en français, anglais et espagnol ;
- cas adversariaux d'injection MCP et d'affirmation juridique non sourcée ;
- documentation de migration V1 à V5, compatibilité, sécurité et checklist de release.

### Corrigé

- ajout du frontmatter officiel manquant aux huit graders introduits en V4 ;
- test de non-régression empêchant désormais la distribution d'un grader sans métadonnées valides.
- rejet des chemins absolus, traversées et liens symboliques dans les manifestes de baseline et de handoff.

### Statut

- contrôles gratuits exécutés ;
- aucun appel modèle ni crédit consommé ;
- release candidate maintenue jusqu'au benchmark comportemental et à la revue humaine finale.

## 4.0.0 — 2026-09-13

### Ajouté

- gouvernance configurable avec rôles, RACI, gates, quorum et journal d'approbations attribuables ;
- baselines SHA-256 vérifiables et références optionnelles de signature externe ;
- politiques d'archivage, de rétention et de redline ;
- tableaux dérivés de couverture et de risque ;
- paquet de handoff avec gate et accusé de réception ;
- journal d'événements append-only et métriques de cycle de vie ;
- outils locaux de baseline, comparaison de versions, tableaux et métriques ;
- agents `governance-reviewer` et `handoff-reviewer` ;
- quatre cas d'évaluation V4, portant le total à quinze.

### Garanties

- aucune identité, approbation ou signature n'est inventée ;
- une empreinte d'intégrité n'est jamais assimilée à une signature ;
- une modification de baseline ou une réception absente bloque le gate ;
- les évaluations par modèle restent différées jusqu'à disponibilité de crédits.

## 3.0.0 — 2026-09-13

### Ajouté

- workflow MCP en deux gates : plan approuvé, puis exécution vérifiée ;
- adaptateurs conceptuels GitHub Issues, Jira, Linear et Notion ;
- plans et journaux de synchronisation JSON ;
- import avec cartographie et préservation de provenance ;
- provenance machine-readable et schémas JSON ;
- détection déterministe des divergences ;
- analyse d'impact transitive des Change Requests ;
- orchestration de recherche sous budget et conditions d'arrêt ;
- gestion multi-juridictions ;
- agents `integration-planner`, `change-impact-analyst` et `jurisdiction-coordinator` ;
- quatre cas d'évaluation V3, portant le total à onze.

### Sécurité

- aucune intégration ou configuration MCP fictive n'est fournie ;
- les contenus MCP sont traités comme non fiables ;
- les suppressions restent séparées et explicitement autorisées ;
- toute écriture est relue et enregistrée sans secret.

### Validation

- onze tests locaux couvrent le validateur, la divergence et l'analyse d'impact ;
- les évaluations par modèle restent différées jusqu'à disponibilité de crédits.

## 2.0.0 — 2026-09-13

### Ajouté

- profils `lean`, `standard` et `regulated` avec sélection validée ;
- extensions pour software, service, internal process et hybrid product ;
- agents `data-ai-expert` et `accessibility-expert` ;
- protocole et modèle de registre des conflits entre agents ;
- validateur de spécification sans dépendance externe ;
- cinq tests automatisés du validateur ;
- sept cas d'évaluation au format officiel Claude Code Plugin Evals.

### Modifié

- routage des agents adapté au profil ;
- mémoire, projet et cahier des charges enrichis avec profil et type ;
- contrôle déterministe demandé avant validation finale lorsque Python 3 est disponible ;
- documentation d'installation et sources actualisées.

### Limite connue

La suite comportementale n'a pas été exécutée dans l'environnement de création : Claude Code 2.1.153 y est installé, alors que `claude plugin eval` exige 2.1.269 ou ultérieur et réalise des appels modèle réels.

## 1.0.0 — 2026-09-13

- Première version du workflow Idea to Spec, de ses douze agents, politiques et huit modèles canoniques.
