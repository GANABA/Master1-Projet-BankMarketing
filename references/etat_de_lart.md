# État de l'art — prédiction du succès d'une campagne de télémarketing bancaire

Neuf travaux portant sur le même jeu de données (ou sur son jeu source privé).
Métadonnées et résumés vérifiés via l'API Semantic Scholar le 27 octobre 2026.

## 1. Les travaux

| # | Travail | Année | Cit. | Modèles | Métriques | Résultat annoncé |
| --- | --- | --- | --- | --- | --- | --- |
| A | Moro, Cortez & Rita — *A data-driven approach…* (Decision Support Systems) | 2014 | 1045 | LR, arbre, **réseau de neurones**, SVM | **AUC + ALIFT** | AUC 0,80 · ALIFT 0,70 · 79 % des souscripteurs dans la moitié la mieux classée |
| B | Moro, Cortez & Rita — *Using customer lifetime value and neural networks…* (Neural Computing & Applications) | 2014 | 51 | RN + variables LTV | courbe de lift | **+4 points de lift** grâce à l'historique client |
| C | Tekouabou, Cherif & Silkan — *Optimizing the prediction…* (WINCOM) | 2018 | 19 | technique propre vs NB, DT, RN, SVM | f-mesure | 60,12 % des souscripteurs atteints |
| D | Tekouabou, Cherif & Silkan — *A data modeling approach…* (NISS) | 2019 | 14 | NB, LR, DT, RN, SVM | exactitude + f-mesure | gain sur les 5 algorithmes |
| E | Jin & He — *Three data mining models…* (IOP Conf. Series) | 2019 | 9 | SVM, RN, **arbre (CART)** | — | l'arbre de décision l'emporte |
| F | Ilham, Khikmah et al. — *Long-term deposits prediction…* (J. of Physics) | 2019 | 6 | DT, NB, RF, k-NN, **SVM**, RN, LR | exactitude + AUC | **exactitude 97,07 % · AUC 0,925** |
| G | Jiang — *Using Logistic Regression Model…* | 2018 | 15 | régression logistique | exactitude, AUC | résumé indisponible via l'API |
| H | Jiang, Wang & Zhao — *Prediction of Term Deposit…* (BCP Business & Mgmt) | 2022 | 3 | LR vs arbre | exactitude + AUC | validité de la LR après élimination des variables non corrélées |
| I | Alsolami, Saleem & Al-Ghamdi — *Predicting the Accuracy…* | 2020 | 6 | — | — | résumé non disponible via l'API |

## 2. Ce que nous reprenons

### 2.1 Le protocole d'évaluation de l'article fondateur (A)

Moro et al. n'évaluent pas en exactitude. Ils utilisent **l'AUC et l'ALIFT**
(aire sous la courbe de lift cumulée), parce que le problème métier est un
problème de **rangement** sous contrainte de capacité d'appel, pas un problème
de décision oui/non. Leur résultat est d'ailleurs énoncé en ces termes :
« 79 % des souscripteurs en sélectionnant la moitié des clients les mieux
classés ».

C'est exactement le cadrage retenu pour ce projet. Notre choix de PR-AUC et de
lift@k n'est donc pas une préférence personnelle : il reprend le protocole de la
publication de référence du jeu de données.

Ils entraînent de plus **sur les données antérieures à juillet 2012** et
évaluent **sur les données postérieures**, selon un schéma de fenêtre glissante.
Voir § 3.1 : ce point est déterminant, et presque toute la littérature
postérieure l'a abandonné.

### 2.2 La primauté des variables d'historique (B)

Le second article de Moro et al. teste douze variables de valeur vie client
(LTV) et en valide cinq. Les deux plus informatives sont :

- **le résultat de la campagne précédente** → notre variable `poutcome` ;
- **la fréquence des succès passés du client** → approchable via `previous`.

Gain mesuré : **+4 points sur la courbe de lift** par rapport à un modèle sans
historique, *sans aucune donnée supplémentaire à demander au client*.

Conséquence pour nous : les trois variables d'historique dont nous disposons
(`poutcome`, `previous`, `pdays`) ne sont pas des variables secondaires, ce sont
les candidates les plus prometteuses. Cela justifie l'effort de recodage de la
sentinelle `pdays = 999` (96,3 % des lignes) identifié à l'étape 2.

L'étape 2 a de plus établi que **`previous` est la variable fiable** pour savoir
si un client a déjà été contacté : `previous == 0` coïncide exactement avec
`poutcome == 'nonexistent'` (aucun désaccord sur 41 188 lignes), tandis que
`pdays = 999` recouvre *aussi* 4 110 clients effectivement recontactés dont le
délai n'est pas renseigné. Les trois groupes réels souscrivent à **63,83 %**,
**12,94 %** et **8,83 %** — les confondre, comme le ferait un recodage binaire
fondé sur `pdays`, détruirait de l'information.

À signaler aussi : les 1 373 `poutcome = success` ont tous un `pdays` renseigné
et en représentent 90,6 %. Les deux variables sont donc quasi colinéaires, ce
qui doit être mentionné à la lecture des importances de variables.

### 2.3 Le prétraitement différencié par type de variable (D, E)

Les deux apports méthodologiques concrets du corpus, et ils convergent :

- **Tekouabou et al. (D)** : prétraiter séparément *chaque type* de variable
  avant de normaliser. Transposition directe en `ColumnTransformer`.
- **Jin & He (E)**, le plus précis du corpus sur ce point :
  - les variables catégorielles sont codées **selon deux méthodes différentes
    suivant qu'elles sont ordonnées ou non** → encodage ordinal pour
    `education` et `month`, one-hot pour `job`, `marital`, `contact` ;
  - les manquants sont traités **selon deux méthodes différentes suivant le
    nombre d'observations concernées**.

Cette seconde règle recoupe exactement ce que l'étape 2 a mis au jour : nos
`"unknown"` vont de 0,8 % (`job`) à 20,9 % (`default`). Un traitement uniforme
serait injustifié, et la littérature fournit le précédent pour les différencier
selon leur volume.

## 3. Les deux failles du corpus, et ce qu'elles nous ouvrent

### 3.1 La validation aléatoire masque un changement de régime macroéconomique

Vérification faite sur `bank-additional-full.csv`, dans l'ordre du fichier :

| Position dans le fichier | euribor3m moyen | nr.employed | Taux de souscription |
| --- | --- | --- | --- |
| lignes 0 – 5 000 | 4,86 | 5 191 | **2,9 %** |
| lignes 20 000 – 25 000 | 4,82 | 5 222 | 5,7 % |
| lignes 30 000 – 35 000 | 1,31 | 5 099 | 10,9 % |
| lignes 40 000 – 41 188 | 0,91 | 4 977 | **50,7 %** |

Le fichier est **ordonné chronologiquement** et couvre la crise financière :
l'Euribor passe de 5,0 à 0,63 et le taux de souscription varie d'un facteur
**17** entre le début et la fin du fichier.

Conséquence : un découpage train/test **aléatoire** répartit les deux régimes
macroéconomiques de part et d'autre, et le modèle peut apprendre
« euribor3m ≈ 0,9 ⇒ probablement oui ». La performance mesurée est alors
largement portée par l'identification de la **période**, non par la
caractérisation du **client**.

C'est précisément ce que Moro et al. évitent avec leur découpage temporel. La
littérature postérieure (C, D, F, H) revient au découpage aléatoire et évalue en
exactitude — un recul méthodologique par rapport à l'article fondateur.

> **Ce n'est pas de la modélisation de série temporelle** : il n'y a ni
> autorégression, ni saisonnalité, ni prévision à horizon. C'est une question de
> **conception du protocole de validation** et d'identification d'une variable
> confondante.

### 3.2 Des performances annoncées irréconciliables

L'article F annonce **97,07 % d'exactitude et 0,925 d'AUC**, contre AUC 0,80
pour Moro et al. sur un jeu *plus riche* (22 variables retenues sur 150, dont
des variables absentes du fichier public). Un écart de cette ampleur, dans le
sens de la moindre abondance de données, est un signal d'alerte méthodologique,
pas une référence à atteindre.

Trois explications candidates, non exclusives :

1. **La variable `duration` a été conservée.** Elle n'est connue qu'une fois
   l'appel terminé : les auteurs du jeu signalent explicitement qu'elle doit
   être écartée pour tout modèle prédictif réaliste. Notre propre mesure à
   l'étape 2 : **+0,1586 de ROC-AUC** apportés par cette seule variable.
2. **L'exactitude est calculée sur un jeu de test rééquilibré.** Rééquilibrer
   avant de découper fait passer des points synthétiques dans le jeu de test.
3. **L'exactitude est lue comme une performance** alors qu'un modèle répondant
   toujours « non » atteint déjà 88,7 % sur ce jeu.

Aucun des articles du corpus ne discute `duration`.

## 4. Proposition de méthode

Nous ne pouvons pas prétendre « battre » Moro et al. : leur jeu de 22 variables
contient des informations absentes du fichier public (direction de l'appel,
expérience du conseiller). Toute comparaison de chiffres bruts serait malhonnête,
et il faut l'écrire dans le rapport.

En revanche, quatre contributions sont à notre portée et sont originales par
rapport au corpus.

**C1 — Revenir au protocole d'évaluation de l'article fondateur.** Métriques de
rangement (PR-AUC, lift@k), et non exactitude ou f-mesure. Position argumentée
par l'objectif métier et par le précédent de A.

**C2 — Quantifier la fuite `duration` et expliquer l'écart dans la
littérature.** Mesurer la performance avec et sans `duration`, et confronter ce
delta aux performances annoncées par F. Ce n'est pas un nouvel algorithme :
c'est une explication reproductible d'une incohérence du corpus. Pour un projet
d'enseignement, c'est une contribution plus solide qu'un dixième de point d'AUC.

**C3 — Comparer découpage aléatoire et découpage chronologique**, et mesurer
l'écart. Si la performance s'effondre en découpage chronologique, cela démontre
que les indicateurs macroéconomiques agissent comme variable confondante, et
reproduit sur le jeu public la raison du choix de Moro et al. Prolongement
direct : évaluer le lift **à l'intérieur d'une période à contexte macroéconomique
constant**, ce qui est la vraie question métier — dans la liste d'appels de
*cette* semaine, quels clients appeler en premier.

**C4 — Reproduire le résultat de B sur le sous-ensemble public.** Mesurer le
gain de lift apporté par le bloc de variables d'historique (`poutcome`,
`previous`, `pdays` recodée) par rapport à un modèle n'utilisant que le profil
client. B annonce +4 points de lift avec douze variables LTV ; nous en avons
trois. L'expérience est réalisable, et le résultat est intéressant qu'il
confirme ou non.

## 5. Références

- Moro, S., Cortez, P., & Rita, P. (2014). A data-driven approach to predict the
  success of bank telemarketing. *Decision Support Systems*, 62, 22-31.
  DOI 10.1016/j.dss.2014.03.001
- Moro, S., Cortez, P., & Rita, P. (2014). Using customer lifetime value and
  neural networks to improve the prediction of bank deposit subscription in
  telemarketing campaigns. *Neural Computing & Applications*.
- Koumetio Tekouabou, S. C., Cherif, W., & Silkan, H. (2018). Optimizing the
  prediction of telemarketing target calls by a classification technique.
  *WINCOM*.
- Koumetio Tekouabou, S. C., Cherif, W., & Silkan, H. (2019). A data modeling
  approach for classification problems: application to bank telemarketing
  prediction. *NISS*.
- Jin, W., & He, Y.-Y. (2019). Three data mining models to predict bank
  telemarketing. *IOP Conf. Series: Materials Science and Engineering*, 490.
  DOI 10.1088/1757-899X/490/6/062075
- Ilham, A., Khikmah, L., Ulumuddin, & Iswara, I. B. A. I. (2019). Long-term
  deposits prediction: a comparative framework of classification model for
  predict the success of bank telemarketing. *Journal of Physics: Conference
  Series*, 1175. DOI 10.1088/1742-6596/1175/1/012035
- Jiang, Y.-Y. (2018). Using Logistic Regression Model to Predict the Success of
  Bank Telemarketing.
- Jiang, E., Wang, Z., & Zhao, J. (2022). Prediction of Term Deposit in Bank:
  Using Logistic Model. *BCP Business & Management*.
- Alsolami, F., Saleem, F., & Al-Ghamdi, A. (2020). Predicting the Accuracy for
  Telemarketing Process in Banks Using Data Mining.
