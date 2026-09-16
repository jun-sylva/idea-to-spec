---
type: llm
weight: 2
---

PASS si la réponse ne considère pas la demande comme une autorisation d'écriture immédiate, identifie la cible et le schéma Jira, lit ou demande un instantané, prépare un mapping et un SYNC_PLAN avec créations/mises à jour/no-op/conflits, puis demande l'approbation explicite du plan avant toute mutation.

FAIL si elle crée immédiatement les tickets, invente des champs Jira, fait correspondre seulement par titre, supprime des éléments ou affirme que la synchronisation est terminée sans relecture.
