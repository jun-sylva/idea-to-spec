---
type: llm
weight: 2
---

# Grader — Redline de versions

PASS si la réponse :

- compare des versions ou baselines identifiées ;
- montre ajouts, retraits et modifications ;
- relie les changements matériels à une Change Request et aux identifiants ;
- distingue différence textuelle et impact sémantique ;
- ne réécrit pas l'historique.

FAIL si elle masque une suppression, écrase une version ou confond différence textuelle et équivalence sémantique.
