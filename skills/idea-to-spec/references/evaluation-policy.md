# Évaluation et critères de release

## Séparation des contrôles

Trois niveaux sont distincts :

1. contrôles structurels gratuits : manifeste, frontmatter, JSON, liens, scripts et tests unitaires ;
2. évaluations comportementales par modèle : activation, respect du workflow et qualité des livrables ;
3. revue humaine : pertinence métier, réglementation et acceptabilité des compromis.

Un niveau ne remplace pas les autres. Ne pas déclarer la qualité comportementale démontrée si les appels modèle n'ont pas été exécutés.

## Comparaison

Exécuter chaque cas dans les mêmes conditions avec et sans plugin : modèle, version Claude Code, date, langue, outils, répétitions et budget. Conserver les sorties brutes, puis normaliser les résultats dans le schéma fourni.

Mesurer au minimum : activation du skill, respect des deux validations, non-implémentation, qualité documentaire, traçabilité, provenance, sécurité, intégrations contrôlées et gouvernance. Présenter taux, effectif, échecs et intervalle ou variabilité lorsque plusieurs répétitions existent.

## Budget et arrêt

Avant exécution, afficher nombre de cas, répétitions, configurations, plafond financier et commande exacte. Obtenir l'autorisation si des crédits sont consommés. Arrêter au plafond, sur erreur d'authentification, ou après trois erreurs d'infrastructure consécutives. Ne pas relancer automatiquement une campagne coûteuse.

## Gate de release

Les seuils sont définis dans le manifeste du benchmark avant l'exécution. Toute modification de seuil après observation des résultats doit être documentée. Un échec de sécurité critique, un contournement de validation ou une action externe non autorisée bloque la release même si la moyenne globale passe.
