# Projet Python for AI — Ciblage d'une campagne de télémarketing bancaire

M1 ISA — Université de Tours.

## Objectif métier

Prioriser les clients à appeler lors d'une campagne de placement d'un dépôt à
terme, sous contrainte de capacité du centre d'appels.

> Pour la liste d'appels de la semaine, retenir les *k* clients les mieux classés
> par le modèle.

Le problème est une classification binaire supervisée, exploitée comme un
problème de rangement. La sortie utile est un score, pas une classe.

## Jeu de données

*Bank Marketing*, UCI Machine Learning Repository, jeu n° 222.

- Page : https://archive.ics.uci.edu/dataset/222/bank+marketing
- DOI : https://doi.org/10.24432/C5K306
- Référence : Moro, S., Cortez, P., & Rita, P. (2014). *A data-driven approach to
  predict the success of bank telemarketing.* Decision Support Systems, 62, 22-31.

Fichier de travail : `data/bank-additional-full.csv` — 41 188 lignes,
20 variables descriptives, séparateur `;`. Taux de souscription : 11,27 %.

## Organisation

```
Projet-BankMarketing/
├── data/         jeu de données brut, non modifié
├── notebooks/    les notebooks, dans l'ordre des étapes de l'énoncé
│   ├── outils.py          fonctions d'affichage (reprises du TD2)
│   └── 01_exploration.ipynb
├── figures/      figures produites par les notebooks
├── references/   état de l’art et articles de référence
└── sorties/      tableaux exportés pour le rapport
```

L’analyse des neuf travaux antérieurs portant sur ce jeu de données, et les
quatre contributions qu’elle nous ouvre, sont dans `references/etat_de_lart.md`.

## Méthode

Les notebooks reprennent la chaîne de traitement des corrections de TD fournies
par l'enseignant.

**Notebook 01 — étape 2 de l'énoncé** (chaîne du TD2) :

`load_and_preview` → `analyze_missing_values` → `analyze_distributions` →
`display_outliers` → `analyze_class_balance`

Deux fonctions sont ajoutées, le jeu *winequality* du TD2 ne comportant aucune
variable catégorielle : `analyze_categorical` et `analyze_target_relation`.

**Notebook 02 — étape 3 de l'énoncé** (fin du TD2) : `analyze_correlations`,
`standard_scaling`, `save_data_and_parameters`. Il retire la variable de fuite,
recode les variables d'historique, traite les `"unknown"`, encode et normalise,
puis produit `sorties/output.csv` et `sorties/params.pkl`, selon le contrat de
passage de relais du TD2 vers le TD3.

Deux écarts assumés par rapport à la correction du TD3, justifiés dans le
notebook :

- le **rééquilibrage est reporté au notebook 03**, après le découpage et sur le
  seul jeu d'apprentissage. Dans l'ordre inverse, SMOTE fait passer des points
  synthétiques dans le jeu de test ;
- **deux protocoles de découpage** sont calculés et conservés, aléatoire et
  chronologique, pour mesurer l'effet du changement de régime macroéconomique
  (taux de souscription : 11,3 % / 11,3 % / 11,3 % en aléatoire, contre
  4,8 % / 11,1 % / 30,8 % en chronologique).

**Notebook 03 — étape 4** (chaîne du TD3) : `load_data_and_parameters` →
`rebalance_classes` → `split_data` → entraînement, réglage et évaluation.

## Décisions prises au cadrage

| Décision | Motif |
| --- | --- |
| `duration` écartée du modèle | Connue seulement après l'appel : fuite de données signalée par les auteurs du jeu |
| Pas d'apprentissage profond | 41 188 lignes tabulaires ; l'énoncé prévient : *no data, no deep learning* |
| Pas de modélisation temporelle | Écartée sur consigne de l'enseignant |
| Accuracy écartée | Un modèle répondant toujours « non » atteint 88,7 % sans valeur |

## Exécution

Les notebooks s'exécutent depuis le dossier `notebooks/`, avec l'environnement
Anaconda (`scikit-learn`, `imbalanced-learn`, `seaborn`). Le Python du Microsoft
Store ne contient pas scikit-learn.

En ligne de commande, le noyau doit être nommé explicitement :

```
jupyter nbconvert --to notebook --execute --inplace         --ExecutePreprocessor.kernel_name=python3 01_exploration.ipynb
```

`sorties/output.csv` et `sorties/params.pkl` ne sont **pas** suivis par Git :
ce sont des fichiers reconstruits par le notebook 02. Après un clone, exécuter
`02_preparation.ipynb` avant `03_modelisation.ipynb`.
