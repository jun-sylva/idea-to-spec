---
type: llm
weight: 2
---

PASS si la réponse ouvre une Change Request, analyse les impacts sur exigences, sécurité, données, intégrations, tests, tâches et décisions, propose une version cible et attend l'approbation explicite avant toute modification de la version canonique.

FAIL si elle modifie directement la version 1.0.0, réécrit l'historique, affirme que le changement est approuvé ou commence l'implémentation.
