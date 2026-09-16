# Politique de validation

## Validation 1 — cadrage

Présenter la compréhension du projet et demander une approbation explicite avant la rédaction complète. Une réponse ambiguë, une nouvelle contrainte ou une simple continuation de conversation ne vaut pas approbation.

Formulation attendue : « Confirmez-vous ce cadrage pour que je prépare le cahier des charges complet ? »

## Validation 2 — résultat final

Après revue interne, présenter la version exacte, les réserves et les questions non critiques. Demander : « Approuvez-vous explicitement cette version du cahier des charges ? »

Tant que l'utilisateur n'a pas répondu sans ambiguïté, utiliser `PENDING_USER_APPROVAL`. Ne jamais écrire soi-même `Approved by user: yes`.

Enregistrer l'approbation dans `governance/APPROVAL_LEDGER.json` avec la version, le rôle, l'identité fournie, la date et une référence de preuve. Pour les règles de quorum ou les rôles spécialisés, lire [governance-policy.md](governance-policy.md). Une approbation d'une version antérieure n'est pas transférable.

## Definition of Ready

Vérifier :

- vision, objectifs et indicateurs définis ;
- utilisateurs, rôles et parcours critiques définis ;
- périmètre inclus et exclu ;
- exigences fonctionnelles et non fonctionnelles testables ;
- sécurité, données et conformité adaptées au risque ;
- critères d'acceptation ;
- dépendances et intégrations ;
- risques et mesures ;
- traçabilité complète ;
- tâches découpées ;
- aucune question critique ouverte ;
- version approuvée explicitement.
- règle du gate applicable satisfaite ;
- baseline de cette version créée et vérifiée.

Si un contrôle échoue, conserver `APPROVED` le cas échéant mais ne pas déclarer `READY_FOR_IMPLEMENTATION`. Expliquer ce qui manque.

## Revue interne

Chercher contradictions, doublons, ambiguïtés, exigences invérifiables, rôles indéfinis, cas limites manquants, lacunes de sécurité, dépendances incohérentes, dérive de périmètre, tâches sans exigence et exigences sans critère d'acceptation.
