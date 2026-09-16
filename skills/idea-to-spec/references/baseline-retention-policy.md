# Baselines, archivage et rétention

## Baseline

Une baseline fige les fichiers canoniques d'une version approuvée au moyen d'un manifeste contenant leurs chemins et empreintes SHA-256. Elle permet de détecter une réécriture ; elle ne prouve pas à elle seule l'identité d'un signataire.

Créer la baseline après satisfaction des approbations applicables. Lui attribuer `BASELINE-x.y.z` et référencer les entrées du journal d'approbation. Ne jamais remplacer un manifeste existant : une correction produit une nouvelle baseline ou une nouvelle version.

Une signature externe peut être référencée par URI, identifiant et fournisseur si elle existe réellement. Sinon utiliser `signature_status: NOT_SIGNED`.

## Vérification

Avant handoff, révision ou synchronisation : recalculer les empreintes, comparer la liste des fichiers et vérifier les approbations référencées. Tout écart place la baseline en `MISMATCH` et bloque le handoff jusqu'à résolution documentée.

## Archivage

Archiver les baselines dans `archive/baselines/<version>/` ou dans le dépôt documentaire déjà adopté. Préserver au minimum le manifeste, les documents canoniques figés, la redline depuis la version précédente, les approbations et le changelog.

Ne pas déplacer ou supprimer automatiquement des documents existants. Prévisualiser toute opération d'archivage et obtenir l'autorisation si elle modifie le projet.

## Rétention

Définir par catégorie : durée, motif, autorité, emplacement, responsable, mode de suppression et suspension légale éventuelle. La durée doit être confirmée ou sourcée ; ne pas inventer une obligation réglementaire.

Une échéance de rétention ne vaut pas autorisation de suppression. Toute suppression reste une action séparée, explicitement autorisée et journalisée.
