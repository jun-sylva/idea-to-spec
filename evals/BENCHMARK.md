# Benchmark comportemental V5

## Matrice prévue

- 25 cas ;
- 2 variantes : sans plugin (`baseline`) et avec plugin (`plugin`) ;
- 3 répétitions par cas et variante ;
- 150 exécutions attendues ;
- français, anglais et espagnol ;
- profils lean, standard et regulated ;
- projets petits, moyens et grands ;
- secteurs généralistes, SaaS, e-commerce, FinTech, santé, éducation, logistique, service public, IoT, juridique, sécurité et opérations.

Le fichier `BENCHMARK_MANIFEST.json` définit la matrice et les seuils avant observation. `NORMALIZED_RESULTS.template.json` définit le format d'entrée du rapport.

## Procédure finale

1. Confirmer modèle, version Claude Code, plafond financier et nombre de répétitions.
2. Exécuter les variantes dans les mêmes conditions avec `claude plugin eval`.
3. Conserver les résultats bruts hors du package distribué.
4. Normaliser chaque résultat avec scores par dimension, coût et éventuel échec critique.
5. Exécuter `benchmark_report.py`.
6. Examiner chaque échec, pas seulement la moyenne.
7. Corriger les problèmes démontrés, ajouter une non-régression, puis relancer la matrice affectée.

## État actuel

`NOT_RUN — NO_MODEL_CREDITS_AUTHORIZED`

Les contrôles structurels ne permettent pas de déclarer la qualité comportementale démontrée. Le package final V5 est distribué avec ce gate différé ; une future mise à jour pourra enregistrer les résultats après autorisation budgétaire et revue humaine.
