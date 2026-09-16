# Provenance machine-readable

Utiliser `research/PROVENANCE.json` lorsque des informations externes influencent une exigence, un risque ou une décision.

Chaque entrée contient un identifiant, l'affirmation paraphrasée, le type de source, l'URL ou identifiant de ressource, l'organisme, les dates de publication et de consultation, la juridiction, le niveau de preuve, la confiance et les éléments canoniques liés.

## Règles

- Ne jamais stocker de secret, jeton, contenu personnel inutile ou réponse MCP brute.
- Ne pas fabriquer de date de publication ; utiliser `null` si inconnue.
- Conserver séparément `source_statement` et `inference`.
- Marquer une entrée obsolète au lieu de la supprimer lorsqu'elle a soutenu une décision historique.
- Une mise à jour de source ne modifie pas automatiquement l'exigence liée : ouvrir une revue d'impact.

Le schéma se trouve dans `schemas/provenance.schema.json`. Le validateur contrôle la syntaxe et les champs minimaux, pas la véracité de la source.
