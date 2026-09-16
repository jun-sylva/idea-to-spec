# Résolution des désaccords entre agents

## Déclencheur

Créer une entrée `CONFLICT-nnn` lorsque deux analyses fiables proposent des conclusions incompatibles qui changent le périmètre, une exigence, la stack, le niveau de risque ou une obligation.

## Traitement

1. Reformuler les deux positions sans les fusionner.
2. Vérifier qu'elles utilisent les mêmes contraintes, dates, versions et juridictions.
3. Comparer preuves, applicabilité, hypothèses, confiance et conséquences.
4. Chercher une source arbitre si elle existe.
5. Classer le conflit : résolu par preuve, résolu par contrainte, choix de compromis, ou décision utilisateur/professionnelle requise.
6. Enregistrer l'arbitrage dans `decisions/AGENT_CONFLICTS.md` et, s'il devient durable, dans `DECISIONS.md`.

Ne pas choisir automatiquement l'avis le plus prudent ou le plus récent : choisir celui qui est le mieux applicable au contexte. Un conflit réglementaire non résolu est bloquant pour le profil `regulated`.

## Restitution

Présenter l'enjeu, les options, les conséquences et la recommandation de l'orchestrateur. Demander validation lorsqu'il s'agit d'un choix de produit ou de risque ; demander un spécialiste habilité lorsqu'il s'agit d'une autorité externe.
