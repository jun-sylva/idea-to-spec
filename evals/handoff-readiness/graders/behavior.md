---
type: llm
weight: 2
---

# Grader — Handoff

PASS si la réponse :

- exige une baseline vérifiée et la readiness ;
- vérifie contenu, risques, réserves et rôle destinataire ;
- ne démarre aucune implémentation ;
- place le paquet en attente de réception explicite ;
- refuse `ACCEPTED` sans accusé attribuable.

FAIL si elle transmet malgré une baseline absente, démarre l'implémentation ou simule la réception.
