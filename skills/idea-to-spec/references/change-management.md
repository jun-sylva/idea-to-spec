# Gestion des changements

## Déclencheur

Toute demande qui altère une version `APPROVED` ouvre une Change Request `CR-nnn`. Ne jamais modifier directement la version canonique.

## Analyse d'impact

Documenter : demande et motivation, exigences touchées, parcours, données, architecture, sécurité, conformité, intégrations, tests, tâches, délais, coûts relatifs, risques, dépendances et décisions remises en cause.

Comparer au moins : refuser le changement, le différer, l'intégrer au périmètre actuel, ou créer un lot séparé lorsque ces options sont réalistes.

## Validation

Présenter l'analyse et la version cible avant toute mise à jour. Attendre une approbation explicite de la Change Request. Après approbation :

1. créer une nouvelle version selon SemVer documentaire ;
2. mettre à jour exigences, tâches, risques et décisions concernés ;
3. ajouter l'entrée au changelog ;
4. refaire les revues et la validation finale ;
5. ne jamais réécrire l'historique de la version approuvée précédente.
6. produire une redline depuis la baseline précédente ;
7. créer une nouvelle baseline et lier ses nouvelles approbations.

## Versioning

- `0.x` : brouillons avant première approbation ;
- `1.0.0` : première spécification approuvée ;
- incrément `MINOR` : fonctionnalité ou évolution compatible de périmètre ;
- incrément `MAJOR` : changement de vision, de contrat ou de périmètre structurant ;
- incrément `PATCH` : clarification sans changement de comportement attendu.
