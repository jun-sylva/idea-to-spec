# Gouvernance et approbations

## Principe

Adapter la gouvernance au risque sans inventer de personnes ni de pouvoirs. L'utilisateur reste l'autorité finale sur le cahier des charges. Les rôles spécialisés donnent un avis ou un visa uniquement si leur responsabilité et leur identité ont été confirmées.

## Rôles configurables

- `sponsor` : arbitre valeur, budget et périmètre ;
- `product` : valide besoins, parcours et priorités ;
- `technical` : valide faisabilité, contraintes et dette acceptée ;
- `security` : valide risques et contrôles de sécurité ;
- `compliance` : valide les obligations identifiées, sans remplacer un professionnel habilité ;
- `user-approver` : donne l'approbation finale explicite.

Une même personne peut tenir plusieurs rôles. Le document doit alors le rendre visible. Un agent, le modèle ou l'orchestrateur ne peut jamais être approbateur humain.

## Niveau de gouvernance

- `lean` : approbation utilisateur finale ; avis spécialisés seulement si un risque l'exige.
- `standard` : produit et technique consultés ou approuvant selon les responsabilités confirmées ; sécurité sur les éléments sensibles.
- `regulated` : produit, technique, sécurité et conformité explicitement attribués ; aucun rôle requis ne peut rester implicite ; revue humaine externe signalée lorsque nécessaire.

## Matrice d'approbation

Pour chaque gate, définir avant la décision : version, rôles requis, règle (`ALL`, `ANY`, `N_OF_M` ou `SINGLE`), quorum, abstentions autorisées, échéance et effet d'un rejet.

Une approbation valide contient : identifiant unique, gate, version exacte, rôle, identité telle que fournie, décision, date, canal ou référence de preuve, et empreinte de baseline lorsqu'elle existe. Ne pas recopier de secret ni de donnée personnelle inutile.

## États

`PENDING` → `APPROVED`, `REJECTED`, `CHANGES_REQUESTED`, `EXPIRED` ou `REVOKED`.

- Une absence de réponse n'est jamais une approbation.
- Une approbation d'une version ne s'applique pas automatiquement à la suivante.
- Une modification de baseline invalide les approbations liées à son empreinte.
- Un rejet ou une demande de changements bloque le gate correspondant.
- Une approbation révoquée reste dans le journal et reçoit une nouvelle entrée de révocation.

## RACI

Définir `Responsible`, `Accountable`, `Consulted`, `Informed` pour les livrables et gates utiles. Chaque ligne doit avoir exactement un `Accountable`. Éviter une matrice exhaustive pour un projet lean ; couvrir au minimum cadrage, spécification, sécurité lorsque pertinente, baseline et handoff.

## Gate final

Le statut `READY_FOR_IMPLEMENTATION` exige : règle d'approbation satisfaite, aucune approbation requise expirée ou révoquée, baseline vérifiée, readiness complet et absence de blocage critique.
