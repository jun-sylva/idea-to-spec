# Analyse d'impact d'une Change Request

## Entrée

La demande, sa motivation, la version approuvée, les identifiants directement concernés et les contraintes nouvelles.

## Couverture

Analyser objectifs, parcours, exigences, données, sécurité, juridictions, architecture, intégrations, risques, décisions, tâches, tests, coûts relatifs et calendrier. Distinguer impact certain, probable et à vérifier.

## Appui déterministe

Exécuter `scripts/analyze_impact.py <projet> --ids <ID...>` pour repérer les identifiants liés dans les documents. Le graphe de cooccurrence peut manquer des relations implicites ; l'agent `change-impact-analyst` complète l'analyse.

## Sortie

Produire `changes/CHANGE_IMPACT.md` : périmètre direct, impacts transitifs, alternatives, risques, migration, stratégie de test, nouvelle version proposée et décisions nécessaires. Attendre l'approbation de la Change Request avant toute mise à jour canonique.
