# Paquet de handoff

## But

Transmettre une spécification approuvée à une équipe d'implémentation ou de test sans autoriser l'implémentation dans ce skill.

## Contenu minimal

- manifeste du paquet et empreintes ;
- baseline approuvée et vérifiée ;
- projet, exigences, tâches, décisions, risques et changelog ;
- matrice de traçabilité et tableaux de couverture ;
- réserves, questions non bloquantes et dette de spécification ;
- contraintes d'environnement et d'intégration ;
- responsabilités de réception ;
- critères d'acceptation du handoff.

Inclure recherche, provenance, juridictions, redlines et journaux d'intégration seulement lorsqu'ils sont pertinents. Ne jamais inclure de secret ni de jeton.

## Gate de transmission

Avant de déclarer `HANDOFF_READY`, vérifier : baseline intacte, approbations satisfaites, `READY_FOR_IMPLEMENTATION`, absence de risque critique non accepté, documents présents, liens résolus et destinataire ou rôle de réception défini.

La réception suit un accusé explicite : `PENDING_RECEIPT` → `ACCEPTED`, `CHANGES_REQUESTED` ou `REJECTED`. L'absence d'accusé ne vaut pas réception.
