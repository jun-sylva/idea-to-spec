# Recherche multi-agent sous budget

## Plan de recherche

Avant délégation, définir : questions, décision soutenue, profondeur, agents, sources prioritaires, délai, nombre maximal de recherches et conditions d'arrêt. Le budget peut être exprimé en `quick`, `standard` ou `deep`, ou par limites explicites fournies par l'utilisateur.

- `quick` : une question, priorité aux sources officielles, un agent, arrêt dès preuve suffisante.
- `standard` : questions indépendantes réparties entre spécialistes, validation ciblée des points critiques.
- `deep` : uniquement sur demande ; plusieurs angles, recherche contradictoire et validation séparée.

## Parallélisme

Paralléliser seulement des questions indépendantes. Ne pas lancer le validateur de sources avant d'avoir les affirmations et références à contrôler. Fournir à chaque agent le minimum de contexte et interdire toute mutation.

## Synthèse

Dédupliquer les sources, rapprocher les dates et juridictions, enregistrer les conflits et attribuer une confiance. Arrêter lorsque l'information supplémentaire ne changerait plus la décision ou lorsque la limite est atteinte. Signaler ce qui n'a pas été recherché.
