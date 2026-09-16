# Gouvernance — [Nom du projet]

## Niveau

- Profil : lean / standard / regulated
- Justification :
- Autorité finale : [identité ou rôle confirmé]

## Rôles

| Rôle | Titulaire confirmé | Responsabilité | Délégation permise | Suppléant |
|---|---|---|---|---|
| user-approver |  | Approbation finale | non |  |
| sponsor |  | Valeur et périmètre |  |  |
| product |  | Besoins et priorités |  |  |
| technical |  | Faisabilité et contraintes |  |  |
| security |  | Risques et contrôles |  |  |
| compliance |  | Obligations identifiées |  |  |

## Gates et règles d'approbation

- Règles machine-readable : [APPROVAL_POLICY.json](APPROVAL_POLICY.json)

| Gate | Objet/version | Rôles requis | Règle | Quorum | Échéance | Effet d'un rejet |
|---|---|---|---|---:|---|---|
| GATE-01 | Cadrage 0.1.0 | user-approver | SINGLE | 1 |  | Retour discovery |
| GATE-02 | Spécification | user-approver | SINGLE | 1 |  | CHANGES_REQUESTED |
| GATE-03 | Handoff |  | ALL |  |  | Bloqué |

## Escalade

- Désaccord non résolu :
- Approbateur indisponible :
- Décision urgente :
- Revue professionnelle obligatoire :
