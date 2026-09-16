# Workflow et modes

## Choisir le mode

### Discovery

À utiliser lorsque l'entrée est une idée encore floue. Clarifier ce qui change réellement la solution, obtenir la validation du cadrage, puis passer en spécification.

### Specification

À utiliser lorsque vision, périmètre et contraintes sont déjà assez stables. Vérifier néanmoins les inconnues critiques avant le premier checkpoint.

### Revision

À utiliser lorsqu'une spécification existe mais n'est pas approuvée. Présenter les impacts de la révision, conserver la traçabilité et demander une nouvelle validation finale.

### Existing project

À utiliser dès qu'un codebase, produit, dépôt ou ensemble documentaire existe. Lire la mémoire et les documents canoniques, inspecter l'existant en lecture seule, comparer comportement et documentation, puis livrer un audit court : état, écarts, dettes, risques, décisions à préserver et questions. Faire valider la compréhension avant de spécifier la suite.

### Change request

À utiliser pour toute modification postérieure à une version `APPROVED`. Lire `change-management.md` avant de proposer une nouvelle version.

## États autorisés

`DRAFT` → `REVIEW` → `PENDING_USER_APPROVAL` → `APPROVED` → `READY_FOR_IMPLEMENTATION`

Si l'utilisateur demande des changements : `USER_CHANGES_REQUESTED` → `REVIEW` → `PENDING_USER_APPROVAL`.

Une approbation confirme une version précise. Une version `APPROVED` ne devient `READY_FOR_IMPLEMENTATION` que si le readiness check est complet.

## Règle de progression

Chaque checkpoint est bloquant. Présenter la proposition, demander validation, puis s'arrêter. Une autorisation générale donnée au début ne vaut pas approbation du cadrage ou du cahier des charges qui n'existait pas encore.

## Sortie de chaque phase

Indiquer :

- version et statut ;
- éléments ajoutés ou modifiés ;
- hypothèses et preuves faibles ;
- décisions attendues ;
- phrase de validation explicite attendue.
