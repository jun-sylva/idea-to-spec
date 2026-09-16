# Mémoire projet

## Lecture

Au début de chaque exécution, chercher `MEMORY.md`. S'il existe, le lire avant l'analyse puis suivre ses liens vers les documents canoniques. Ne jamais se fier au seul résumé lorsqu'une décision ou une exigence précise est en jeu.

## Hiérarchie de vérité

1. Version approuvée de `requirements/REQUIREMENTS.md`
2. `decisions/DECISIONS.md`
3. `planning/TASKS.md` et `risks/RISK_REGISTER.md`
4. `CHANGELOG.md`
5. `MEMORY.md`, qui n'est qu'un index synthétique

Les manifestes de baseline attestent l'intégrité d'une version donnée sans remplacer son contenu. Le journal d'approbation établit qui a décidé quoi ; le journal d'événements fournit la chronologie. Ils sont append-only et ne modifient pas la hiérarchie documentaire ci-dessus.

En cas de conflit, ne pas écraser silencieusement. Signaler l'écart, retrouver l'approbation la plus récente et demander confirmation si l'autorité reste ambiguë.

## Écriture

Mettre à jour la mémoire à la fin d'une phase validée ou lorsqu'un fait durable est confirmé. Ne pas y copier le cahier des charges. Conserver : identité du projet, vision, phase, version canonique, décisions validées, contraintes, préférences, questions en attente, risques principaux et liens relatifs.

Ne jamais enregistrer de secret, jeton, mot de passe, donnée personnelle inutile ou contenu de source sous licence au-delà de ce qui est nécessaire.
