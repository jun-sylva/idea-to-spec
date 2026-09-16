# Découpage et traçabilité

## Hiérarchie

`EPIC-nn` → `FEAT-nn.nn` → `US-nn.nn.nn` → `TASK-nn.nn.nn-X` → `TEST-nn.nn.nn-nn`

Chaque user story suit la forme : « En tant que [rôle], je veux [capacité] afin de [résultat]. » Ne pas forcer ce format pour une tâche technique qui n'exprime pas un besoin utilisateur.

## Contenu d'une tâche

- identifiant et titre orienté résultat ;
- objectif et limites ;
- exigences couvertes ;
- dépendances et prérequis ;
- livrable observable ;
- critères d'acceptation ou référence aux tests ;
- risques ou compétences requises ;
- estimation relative si l'utilisateur la demande, avec hypothèses.

## Matrice de traçabilité

Chaque `FR`, `NFR` et `SEC` doit pointer vers au moins un critère d'acceptation et, lorsqu'il implique du travail, une story ou tâche. Toute tâche doit justifier l'exigence ou le risque qu'elle traite. Signaler les éléments orphelins.

## Ordonnancement

Découper par résultats vérifiables. Identifier le chemin critique, les travaux parallélisables, les dépendances externes et les gates de sécurité ou conformité. Ne pas transformer la roadmap en promesse calendaire sans capacité d'équipe confirmée.
