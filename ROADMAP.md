# Roadmap — Idea to Spec

## V1.0 — Socle livré

Objectif : produire une spécification fiable à partir d'une idée ou d'un projet existant, sans implémentation.

Inclus :

- quatre modes : discovery, specification, revision, existing project ;
- audit préalable de l'existant ;
- mémoire synthétique et sources de vérité séparées ;
- validations intermédiaire et finale bloquantes ;
- statuts et versioning documentaire ;
- Change Requests après approbation ;
- exigences fonctionnelles, non fonctionnelles et sécurité identifiées ;
- découpage Epic → Feature → Story → Task → Test ;
- matrice de traçabilité et Definition of Ready ;
- recherche sourcée, hiérarchie des sources, preuve et confiance ;
- recommandation de stack comparative sans implémentation ;
- douze agents spécialisés activés à la demande ;
- politique MCP sûre et indépendante de fournisseurs ;
- modèles des huit documents demandés.

Limites assumées : la qualité n'a pas encore été mesurée sur un corpus d'évaluations ; les experts sectoriels couvrent six domaines ; aucune intégration Jira, Linear, Notion, GitHub ou base métier n'est fournie ; la validation professionnelle reste externe pour les enjeux réglementaires, médicaux ou financiers.

## V2.0 — Personnalisation et infrastructure de qualité — LIVRÉE

Priorité : rendre la qualité observable et adapter la profondeur sans alourdir tous les projets.

- [x] suite de sept évaluations réalistes : idée simple, SaaS, e-commerce, FinTech, santé, projet existant et Change Request ;
- [ ] mesures comparatives avec/sans plugin : en attente de Claude Code v2.1.269+ et d'une autorisation d'appels modèle ;
- [x] profils de profondeur `lean`, `standard` et `regulated` ;
- [x] extensions pour logiciel, service, processus interne et produit hybride ;
- [x] validateur déterministe des identifiants, traçabilité, statuts et questions bloquantes ;
- [x] expert données/IA et expert accessibilité ;
- [x] registre des conflits entre agents et justification de l'arbitrage.

État : fonctionnalités V2 livrées. Le benchmark reproductible reste à exécuter avant de considérer la qualité comportementale comme mesurée.

## V3.0 — Intégrations contrôlées et collaboration — LIVRÉE

Priorité : connecter le cahier des charges aux outils de travail sans perdre l'autorité utilisateur.

- [x] protocole MCP optionnel avec lecture, prévisualisation, autorisation, écriture, relecture et journal ;
- [x] adaptateurs conceptuels pour GitHub Issues, Jira, Linear, Notion et outils équivalents ;
- [x] synchronisation idempotente fondée sur des identifiants canoniques ;
- [x] détection locale des divergences entre spécification et instantané externe ;
- [x] import avec carte, provenance, contradictions et validation d'autorité ;
- [x] recherche multi-agent avec profondeur et conditions d'arrêt ;
- [x] provenance machine-readable et schéma JSON ;
- [x] support multi-juridictions avec socle, variantes et conflits ;
- [x] analyse d'impact déterministe et experte des Change Requests ;
- [x] trois agents V3 et quatre scénarios d'évaluation supplémentaires ;
- [ ] exécution des évaluations reportée à la phase finale faute de crédits.

État : fonctionnalités et tests locaux V3 livrés. Les écritures réelles dépendent des MCP installés par l'utilisateur et restent soumises à autorisation au moment de l'action.

## V4.0 — Gouvernance d'équipe et cycle de vie — LIVRÉE

- [x] rôles de validation configurables : produit, technique, sécurité, conformité et sponsor ;
- [x] matrices RACI et règles d'approbation adaptées au niveau de risque ;
- [x] comparaison de versions et redlines lisibles ;
- [x] baselines vérifiables, références de signature externe, archivage et politique de rétention ;
- [x] tableaux de couverture et de risque évolutifs ;
- [x] paquet de handoff standardisé pour équipes d'implémentation et de test ;
- [x] observabilité du workflow : décisions en attente, temps de cycle, changements de scope et dette de spécification ;
- [x] deux agents spécialisés et quatre scénarios d'évaluation V4 ;
- [ ] exécution des évaluations par modèle reportée à la phase finale faute de crédits.

Critère de sortie : les approbations sont attribuables, les historiques ne sont pas réécrits et un audit peut reconstruire pourquoi chaque exigence existe.

État : fonctionnalités et contrôles locaux V4 livrés. Une empreinte garantit l'intégrité, pas l'identité ; une signature n'est déclarée que si un service externe réel est référencé.

## V5.0 — Validation comportementale et durcissement final — LIVRÉE

- [ ] exécuter le benchmark avec/sans plugin sur l'ensemble des cas lorsque des crédits sont disponibles ;
- [x] définir les mesures d'activation, gates, qualité, provenance, sécurité, intégrations, gouvernance et localisation ;
- [x] préenregistrer les seuils et fournir l'agrégateur de résultats ;
- [x] ajouter des cas de non-régression pour l'anomalie de graders V4 ;
- [x] couvrir 25 cas, 3 langues, 3 profils, 3 tailles et plusieurs secteurs ;
- [x] documenter la migration V1 → V5 et la compatibilité Claude Code ;
- [x] effectuer la revue de sécurité locale et préparer la release candidate ;
- [ ] corriger les faiblesses comportementales observées après la campagne réelle ;
- [ ] effectuer la revue humaine finale.

Critère de sortie : les critères de la version finale sont démontrés par des résultats reproductibles, pas seulement par la présence des fichiers.

État : `5.0.1`. Toute l'infrastructure, les contrôles gratuits, la matrice, la documentation bilingue et les diagrammes explicatifs sont livrés. Le benchmark comportemental reste volontairement différé afin de ne consommer aucun crédit sans autorisation.

## Version finale — PACKAGE LIVRÉ

La version finale n'est pas un nombre d'agents. Elle est atteinte lorsque le système satisfait durablement ces critères :

- comportement évalué sur plusieurs secteurs, langues et niveaux de complexité ;
- aucune affirmation critique non sourcée présentée comme un fait ;
- recherche reproductible avec fraîcheur, juridiction et confiance visibles ;
- deux validations et Change Requests appliquées sans contournement ;
- traçabilité bidirectionnelle complète de l'objectif au test ;
- accessibilité, sécurité, confidentialité et conformité intégrées proportionnellement au risque ;
- intégrations réversibles, idempotentes et soumises au moindre privilège ;
- modèles extensibles sans alourdir le contexte de tous les projets ;
- documentation de migration et compatibilité maintenues avec les versions supportées de Claude Code ;
- revue humaine obligatoire clairement signalée pour toute décision à fort impact.

À ce stade, les évolutions deviennent incrémentales : nouveaux modules sectoriels fondés sur des besoins observés, maintenance des sources, compatibilité et amélioration continue des évaluations.

Le package final V5 est distribué avec transparence : les critères structurels et de sécurité locale sont contrôlés, tandis que la maturité comportementale ne sera considérée comme démontrée qu'après exécution du benchmark et revue humaine.

Prochaine décision facultative : autoriser ultérieurement le budget du benchmark, analyser ses résultats puis publier une mise à jour de maintenance si des corrections observables sont nécessaires.
