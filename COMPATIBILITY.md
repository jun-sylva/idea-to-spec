# Compatibilité Claude Code

## Versions

| Fonction | Version minimale documentée | Vérification V5 |
|---|---:|---|
| Chargement du plugin et du skill | version récente prise en charge | Claude Code 2.1.270 : PASS |
| `claude plugin validate` | 2.1.233+ | Claude Code 2.1.270 : PASS |
| `claude plugin eval` | 2.1.269+ | commande disponible ; appels modèle non exécutés |

## Dépendances locales

- Python 3 pour les validateurs et rapports déterministes ;
- bibliothèque standard Python uniquement ;
- aucun serveur MCP, secret ou fournisseur imposé ;
- les agents utilisent uniquement les champs de frontmatter pris en charge pour un plugin.

## Politique de maintenance

Avant une release, vérifier la documentation officielle Claude Code, exécuter `claude plugin validate`, la suite unitaire, `validate_evals.py` et `security_audit.py`. Toute incompatibilité observée doit être documentée avant modification des manifestes ou agents.
