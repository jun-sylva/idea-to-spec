# Projets multi-juridictions

## Modèle

Séparer :

- socle commun du produit ;
- variantes par pays ou région ;
- règles dépendant du rôle juridique de l'organisation ;
- exigences contractuelles distinctes de la loi ;
- points nécessitant une validation professionnelle locale.

## Traitement

1. Identifier pays de l'organisation, utilisateurs, traitement, hébergement, paiement et livraison.
2. Ne pas supposer qu'un texte d'une juridiction s'étend aux autres.
3. Utiliser des identifiants suffixés si le comportement diffère, par exemple `FR-012-EU` et `FR-012-US`.
4. Documenter les conflits de règles, stratégie de géorestriction ou localisation, preuve et propriétaire de validation.
5. Bloquer le readiness réglementé si une juridiction de lancement n'a pas de revue adaptée.

Consigner la matrice dans `compliance/JURISDICTIONS.md` et déléguer à `jurisdiction-coordinator` lorsque plus d'une juridiction affecte le comportement.
