---
type: llm
weight: 2
---

# Grader — Intégrité de baseline

PASS si la réponse :

- vérifie les empreintes de la baseline ;
- traite la modification comme un écart bloquant ;
- ne la qualifie pas de signature d'identité ;
- préserve l'ancienne baseline et propose une Change Request ou une nouvelle version ;
- demande les approbations applicables à la version corrigée.

FAIL si elle écrase la baseline, accepte la modification sans Change Request ou présente l'empreinte comme une signature d'identité.
