# Adaptateurs conceptuels

Les noms d'outils MCP varient selon le serveur. Découvrir leur schéma réel au lieu d'inventer des appels. Ces mappings décrivent les concepts à préserver.

## GitHub Issues

- `TASK` ou `US` → issue ; dépendances et exigences → corps ou liens.
- Jalons ou labels peuvent représenter lot, priorité et type si l'utilisateur valide cette convention.
- Conserver un marqueur stable `Idea-to-Spec-ID: TASK-...` dans un champ recherchable.

## Jira

- `EPIC`, `US`, `TASK` → types Jira disponibles dans le projet cible.
- Vérifier les champs obligatoires, statuts et schémas avant le plan.
- Ne pas supposer qu'un statut local possède un équivalent exact.

## Linear

- Lot/feature → project ou initiative selon l'espace ; tâche/story → issue.
- Vérifier équipes, cycles, labels et états disponibles.
- Ne pas assigner de personne sans instruction explicite.

## Notion

- Spécification → page ou base existante ; éléments traçables → lignes seulement si la structure cible s'y prête.
- Préserver titres, identifiants et relations sans transformer silencieusement la structure du document.

## Autre outil

Établir un mapping explicite entre identifiant canonique, objet externe, état, liens et champs obligatoires. Si aucune correspondance fiable n'existe, proposer un export ponctuel plutôt qu'une fausse synchronisation.
