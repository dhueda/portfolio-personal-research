# Portfolio de recherche personnelle

Deux projets courts en méthodes quantitatives, réalisés en Python. Ils portent sur l'IA, le travail et le dialogue social. Ils sont exploratoires : chaque projet décrit ses limites dans son propre README.

| Projet | Question | Données | Méthodes |
|---|---|---|---|
| [`ai-adoption-bargaining`](ai-adoption-bargaining) | Les pays où la négociation collective couvre plus de salariés adoptent-ils l'IA différemment ? | Eurostat (adoption de l'IA par les entreprises), couverture de la négociation collective, PIB par habitant | Nettoyage avec pandas, nuage de points, corrélations, régression simple |
| [`presse-ia-travail`](presse-ia-travail) | Comment la presse française parle-t-elle de l'IA et du travail depuis 2024 ? | 2 865 titres de presse (Google Actualités, janvier 2024 à octobre 2026) | Collecte par flux RSS, indicateurs lexicaux, régression avec effets fixes par média |

## 1. ai-adoption-bargaining

Étude de la relation entre la négociation collective et l'adoption de l'IA dans les entreprises européennes.

- Données publiques Eurostat, téléchargées puis nettoyées avec pandas.
- Analyse : nuage de points, corrélations, régression simple, puis ajout du PIB par habitant comme variable de contrôle.
- Le notebook est `01_ai_bargaining_analysis.ipynb`. Le README du dossier est en anglais.
- Statut : version 1, à compléter.

## 2. presse-ia-travail

Exploration computationnelle des titres de presse française sur l'IA et le travail.

- Collecte de 5 923 articles, puis 2 865 titres après filtrage.
- Trois hypothèses testées : hausse du volume, place de la menace pour l'emploi, rôle des plans de suppression d'emplois.
- Test de robustesse : régression avec effets fixes par média.
- Les limites sont détaillées dans le README du dossier. Les indicateurs sont lexicaux et n'ont pas été validés manuellement.

## Outils

Python, pandas, matplotlib, scikit-learn, statsmodels.

## Lien avec mes recherches

Ces projets s'inscrivent dans mon intérêt pour le travail, l'IA et le rôle du dialogue social. Le premier regarde les différences entre pays. Le second regarde le discours des médias.
