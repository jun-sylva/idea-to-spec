# Migration de V3 vers V4

[Read in English](MIGRATION_V3_TO_V4.md)

La V4 conserve les documents V3 et ajoute une couche de gouvernance. Ne pas recréer ni réécrire une version déjà approuvée.

## Projet en cours de cadrage ou de revue

1. Copier les nouveaux modèles dans les dossiers appropriés.
2. Définir `governance/GOVERNANCE.md`, `RACI.md` et `APPROVAL_POLICY.json` avec l'utilisateur.
3. Initialiser `APPROVAL_LEDGER.json` sans inventer d'approbation passée.
4. Continuer le workflow puis créer la première baseline après approbation.

## Projet déjà approuvé en V3

1. Conserver la version et son historique.
2. Enregistrer les preuves d'approbation existantes uniquement si elles sont retrouvables et attribuables ; sinon les marquer comme héritées à confirmer.
3. Créer une baseline initiale de migration, identifiée comme telle dans le changelog.
4. Vérifier les empreintes et exécuter le validateur V4.
5. Ne pas prétendre que la baseline était signée ou existait au moment de l'approbation V3.

## Handoff

Créer le paquet uniquement pour une version `READY_FOR_IMPLEMENTATION` avec baseline vérifiée. Une transmission déjà réalisée avant V4 reste historique ; ne pas fabriquer rétroactivement un accusé de réception.

## Compatibilité

Les fichiers V3 de recherche, provenance, juridiction, import et synchronisation restent inchangés. Les intégrations externes continuent d'exiger une prévisualisation et une autorisation au moment de l'écriture.
