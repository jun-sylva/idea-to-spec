# Validateur déterministe

Le script `scripts/validate_spec.py` vérifie la structure observable du dossier de spécification. Il n'évalue pas la pertinence métier.

## Utilisation

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/validate_spec.py" /chemin/du/projet
python3 "${CLAUDE_SKILL_DIR}/scripts/validate_spec.py" /chemin/du/projet --json
python3 "${CLAUDE_SKILL_DIR}/scripts/validate_spec.py" /chemin/du/projet --strict
```

## Contrôles

- présence des documents canoniques ;
- version, statut et profil de la spécification ;
- identifiants en doublon dans les titres ;
- couverture des exigences `FR`, `NFR` et `SEC` par le plan des tâches ;
- tâches sans lien vers une exigence ou un risque ;
- cases Definition of Ready ;
- approbation et questions bloquantes incompatibles avec `READY_FOR_IMPLEMENTATION` ;
- présence du dossier de recherche pour un profil `regulated`.
- syntaxe et champs minimaux de `PROVENANCE.json`, `SYNC_PLAN.json` et `SYNC_LEDGER.json` lorsqu'ils existent ;
- provenance obligatoire pour un profil `regulated` ;
- absence de plan de synchronisation en attente au passage en readiness.

Code de sortie : `0` sans erreur, `1` avec erreur. En mode `--strict`, les avertissements font également échouer la commande. Examiner les résultats au lieu de modifier les documents uniquement pour satisfaire le script.
