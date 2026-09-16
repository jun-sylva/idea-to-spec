# Observabilité du workflow

## Journal d'événements

Enregistrer uniquement les événements utiles au pilotage : création de phase, demande et décision d'approbation, changement de statut, ouverture et décision de Change Request, création/vérification de baseline, variation de périmètre, détection/résolution de dette, préparation/réception du handoff.

Chaque événement contient un identifiant, un type, une date ISO 8601, un acteur ou rôle, la version, les identifiants liés et une référence de preuve. Le journal est append-only. Une correction ajoute un événement compensatoire.

## Mesures dérivées

- temps de cycle par phase ou gate lorsque début et fin existent ;
- nombre de décisions en attente et leur ancienneté ;
- nombre de Change Requests par version ;
- ajouts et retraits d'exigences pour rendre visible la dérive de périmètre ;
- dette de spécification ouverte, résolue et vieillissante ;
- état du handoff et des baselines.

Toujours afficher la période, le nombre d'événements et les données manquantes. Ces mesures décrivent le workflow ; elles ne mesurent pas la productivité individuelle et ne doivent pas servir seules à évaluer une personne.

## Minimisation

Préférer les rôles ou identifiants fournis aux données personnelles. Ne pas enregistrer les messages complets lorsque la référence d'approbation suffit.
