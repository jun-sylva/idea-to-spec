# Routage des agents

## Principes

Déléguer une question autonome avec le contexte minimal suffisant : objectif, contraintes confirmées, juridiction, horizon temporel, format de retour et exclusions. Ne pas déléguer la décision finale ni la relation utilisateur.

Ne pas appeler tous les agents. Employer le plus petit ensemble couvrant les risques réels. Les travaux indépendants peuvent être lancés en parallèle ; les validations de source doivent suivre la recherche qu'elles évaluent.

## Agents transversaux

- `research-specialist` : collecte actuelle et sourcée.
- `source-validator` : vérification des affirmations critiques et des citations.
- `solution-architect` : comparaison de stacks sous contraintes.
- `security-compliance-reviewer` : exigences de sécurité, vie privée et conformité ; ne remplace pas un avis juridique ou médical.
- `data-ai-expert` : données, qualité, gouvernance, analytique et systèmes d'IA.
- `accessibility-expert` : exigences d'accessibilité et critères vérifiables adaptés aux parcours.
- `integration-planner` : mapping et plan de synchronisation en lecture seule.
- `change-impact-analyst` : impacts directs et transitifs d'une Change Request.
- `jurisdiction-coordinator` : socle, variantes et conflits multi-juridictions.
- `governance-reviewer` : rôles, RACI, quorum, approbations et baselines avant un gate.
- `handoff-reviewer` : intégrité et exploitabilité du paquet avant transmission.
- `devil-advocate` : contradictions, irréalisme, complexité et angles morts.
- `specification-reviewer` : qualité, cohérence, testabilité, traçabilité et readiness.

## Experts sectoriels

Activer seulement si le domaine est central : `fintech-expert`, `healthcare-expert`, `ecommerce-expert`, `saas-expert`, `marketing-expert`, `legal-regulatory-expert`.

Un projet multi-domaine peut justifier plusieurs experts. Demander à chacun de distinguer obligations, pratiques courantes, recommandations et questions nécessitant un professionnel habilité.

## Routage par profil

- `lean` : déléguer uniquement lorsqu'une inconnue change le cadrage ou lorsqu'un risque impose un spécialiste.
- `standard` : utiliser les spécialistes correspondant aux fonctions et risques centraux.
- `regulated` : recherche et validation de sources séparées, revue sécurité/conformité obligatoire, expert sectoriel adapté et revue humaine explicitement requise.

## Contrat de retour

Exiger : résumé, constats numérotés, preuves et dates lorsqu'elles existent, hypothèses, niveau de confiance, risques, recommandations avec compromis, questions ouvertes et éléments proposés pour les exigences. L'orchestrateur vérifie les conflits avant intégration.

Tout conflit matériel suit [conflict-resolution.md](conflict-resolution.md) et reste visible jusqu'à son arbitrage.

Avant `READY_FOR_IMPLEMENTATION` sur un projet standard ou regulated, utiliser `governance-reviewer`. Avant `HANDOFF_READY`, utiliser `handoff-reviewer`. Pour un projet lean, appliquer localement ces contrôles sans délégation si la structure reste simple.
