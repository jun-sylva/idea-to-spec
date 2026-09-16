# Synchronisation et divergences

## Autorité

La spécification approuvée est canonique pour le besoin. Un outil de tickets peut être canonique pour l'état d'exécution uniquement si cette règle est décidée et enregistrée.

## Identité et idempotence

Chaque objet externe porte un identifiant canonique stable. Ne jamais faire correspondre uniquement par titre. Une nouvelle exécution avec même identifiant, même version source et même empreinte doit produire `NO_OP`.

## Types d'écart

- `MISSING_EXTERNAL` : élément canonique absent de la cible.
- `UNKNOWN_EXTERNAL` : élément externe sans correspondance canonique.
- `TITLE_CHANGED` ou `CONTENT_CHANGED` : projection divergente.
- `STATE_CONFLICT` : états incompatibles selon la convention décidée.
- `STALE_READ` : cible modifiée après préparation du plan.

Les suppressions ne sont jamais automatiques. Présenter archivage, détachement ou conservation comme options.

## Détection

Exporter un instantané normalisé à partir de `templates/EXTERNAL_SNAPSHOT.json`, puis utiliser `scripts/detect_drift.py`. Son résultat est un diagnostic : l'orchestrateur examine chaque écart et prépare un plan soumis à approbation.
