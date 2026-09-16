# Profils de profondeur

Le profil règle la profondeur documentaire et les gates ; il ne réduit jamais les exigences de sécurité ou de conformité réellement applicables.

## Lean

Pour une exploration, un prototype ou un petit projet réversible, avec peu d'acteurs, aucune donnée fortement sensible et un impact limité.

- Documents courts, centrés sur le problème, le périmètre, les parcours critiques et les critères d'acceptation.
- Recherche seulement pour les hypothèses déterminantes.
- Décomposition au niveau permettant le prochain lot de travail.
- Revue spécialisée uniquement lorsqu'un risque précis l'exige.

Ne pas utiliser pour paiements, santé, décisions automatisées à fort impact, activité réglementée, données très sensibles ou dépendance critique mal comprise.

## Standard

Profil par défaut pour un produit ou service destiné à être construit et maintenu.

- Ensemble documentaire complet et proportionné.
- Recherche sur les faits externes importants.
- Architecture comparée lorsque la technologie est structurante.
- Traçabilité, risques, sécurité et revue contradictoire avant validation finale.

## Regulated

Pour un produit à fort impact ou soumis à obligations sectorielles, juridiques, contractuelles ou de sécurité renforcées.

- Source primaire prioritaire et validation indépendante des affirmations critiques.
- Juridiction, version, applicabilité et preuve enregistrées.
- Revue sécurité/conformité et expert sectoriel obligatoires.
- Aucune décision critique fondée uniquement sur une confiance `LOW`.
- Validation humaine qualifiée identifiée comme gate ; le skill ne s'y substitue pas.
- Traçabilité complète des objectifs aux tests et preuves.

## Sélection et changement

Proposer le profil à partir du niveau d'impact, de la sensibilité des données, de la réversibilité, du nombre d'acteurs, des obligations et du coût d'une erreur. Expliquer la recommandation en deux ou trois phrases et la faire confirmer lors de la validation du cadrage.

Un profil choisi par l'utilisateur est une décision. Si de nouveaux risques rendent le profil insuffisant, recommander une élévation et demander validation. Ne pas abaisser un profil sans exposer ce qui serait retiré.

Les compléments prêts à copier se trouvent dans `templates/profiles/`.
