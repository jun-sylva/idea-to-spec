# Migration V1 à V5

[Read in English](MIGRATION_V1_TO_V5.md)

Cette migration ajoute des contrôles sans invalider les documents historiques. Ne jamais fabriquer rétroactivement une approbation, une provenance, une baseline ou une réception.

## Depuis V1

1. Conserver `MEMORY.md`, `PROJECT.md`, exigences, tâches, décisions, recherche, risques et changelog.
2. Ajouter profil et type de projet V2, puis exécuter le validateur pour révéler les lacunes sans les corriger silencieusement.
3. Ajouter la provenance structurée uniquement pour les sources retrouvables.
4. Déclarer les intégrations et juridictions réellement applicables.
5. Installer la gouvernance V4 avec rôles confirmés, RACI et règles de gate.
6. Créer une baseline de migration de l'état actuel ; ne pas prétendre qu'elle existait à l'époque de l'approbation.

## Depuis V2

Conserver profils, extensions, conflits et identifiants. Ajouter les artefacts V3 d'intégration ou de provenance seulement lorsqu'ils sont utilisés, puis appliquer la gouvernance V4.

## Depuis V3

Suivre `MIGRATION_V3_TO_V4.md`, puis adopter les politiques V5 de contenu non fiable, localisation et évaluation.

## Depuis V4

Mettre à jour le plugin sans modifier les baselines de projet. Ajouter les politiques V5, les outils d'audit et la nouvelle suite d'évaluation. Les approbations V4 restent valides pour leur version et leur empreinte exactes.

## Vérification

Exécuter les tests locaux, le validateur de spécification, le validateur des évaluations, l'audit de sécurité et la validation native du plugin. Les projets `READY_FOR_IMPLEMENTATION` doivent continuer à satisfaire leurs gates V4.

## Retour arrière

Conserver l'archive de la version précédente. Un retour au plugin antérieur ne doit jamais supprimer les artefacts V3/V4/V5 ; les anciennes versions peuvent les ignorer, mais ne doivent pas les réécrire.
