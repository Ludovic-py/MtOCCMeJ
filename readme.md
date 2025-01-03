# Cable v4.1

Conçue par Raphaël
Cable v4.1 est une application graphique de câblage interactive avec la gestion logique des câbles. Les utilisateurs peuvent créer, modifier et analyser des configurations de câbles afin de déterminer la fiabilité et l'intégrité du système. Elle est accompagnée de fonctionnalités de visualisation des états logiques des sorties en expressions booléennes ou fonctions.

# Cable v4_1

une tentative d'optimisation du programme precedent par moimême avec l'utilisation de liste pour l'optimisation (lines.append) work in-progress

# dynamic trust table

programme ayant pour but de donner une table des input et output necessaire afin d'obtenir un cablage correct et fiable 

(sera prochainnement utilisé en tant que module pour un programme de test automatique)


---

## Features (Cable 4.1)

### Fonctionnalités principales :
- **Création dynamique de câbles** :
  - Les utilisateurs saisissent le nombre de câbles lors de l'initialisation.
  - Le programme ajuste automatiquement l'espacement et l'apparence des câbles dans l'interface graphique.

- **Connexion des câbles** :
  - Reliez les câbles par des liens verticaux pour représenter des relations logiques.
  - **Clic gauche** pour :
    - Créer des liens entre deux câbles (l'un au-dessus de l'autre).
    - Supprimer des liens existants en cliquant directement sur le lien.

- **Sortie graphique** :
  - Effectuez un clic droit sur un câble pour ouvrir une fenêtre distincte affichant son état logique sous forme de :
    - **Expressions booléennes**
    - **Mode fonction** (pas encore utilisable).

- **Analyse de fiabilité** :
  - Vérifie automatiquement la fiabilité du câblage pour confirmer la cohérence logique.
  - Affiche l'état de fiabilité :
    - `"Le câblage est fiable."` (Le câblage est fiable).
    - `"Le câblage n'est pas fiable."` (Le câblage n'est pas fiable).

- **Interface graphique dynamique** :
  - Redimensionnement dynamique des éléments pour adapter l'interface graphique à la taille de l'écran.
  - Modes d'affichage ajustables pour les expressions logiques et les câbles.
---

## How to Use

### Exécution du programme :
1. Lancez `Cable v4.1` depuis le terminal ou un IDE Python.
2. Une boîte de dialogue apparaîtra, vous permettant de saisir le nombre de câbles souhaité.
3. Une fois saisi, l'interface graphique principale affichera les câbles.

### Opérations :

1. **Créer des liens** :
   - Cliquez sur un câble, puis sur un autre câble directement au-dessus ou en dessous pour former un lien logique.

2. **Supprimer des liens** :
   - Cliquez sur un lien vertical existant pour le supprimer.

3. **Afficher les sorties des câbles** :
   - Faites un clic droit sur un câble pour ouvrir une nouvelle fenêtre affichant son état logique, soit sous forme de sortie booléenne, soit sous forme de fonction.

4. **Analyse de fiabilité** :
   - Un état de fiabilité sera affiché en bas de l'interface principale et sera mis à jour dynamiquement en fonction des modifications effectuées.
---

## Conception de l'application

Ci-dessous se trouvent les principaux composants du programme :

### **1. Interface graphique (Tkinter)**
- Gère la disposition graphique des câbles et des éléments associés dans l’application (GUI).

- **L'ordre des connexions est important** lors des tests, mais les connexions elles-mêmes sont non dirigées.
    - Par exemple, la séquence `(1,2)` puis `(3,2)` est différente de `(3,2)` puis `(1,2)`, même si les connexions individuelles `(1,2)` ou `(3,2)` sont traitées de la même manière peu importe leur direction (puisqu'elles sont non dirigées).

En d'autres termes, nous **testons des séquences spécifiques sur la manière dont les connexions sont appliquées**, tout en traitant les connexions individuelles comme `(1,2)` et `(2,1)` de manière identique.

## Design de l'application (Suite)

1. Chaque câble possède une **sortie** qui dépend de la logique booléenne appliquée aux entrées qu'il reçoit.
    - Par exemple :
        - La **sortie du câble supérieur** peut être calculée en utilisant un `OR` (équivalent à `max` en logique booléenne).
        - La **sortie du câble inférieur** peut être calculée en utilisant un `AND` (équivalent à `min` en logique booléenne).

2. **Fiabilité via les sorties :**
    - Le système peut être testé pour sa fiabilité en vérifiant si les sorties booléennes de chaque câble correspondent aux sorties attendues dans des conditions d'entrée spécifiques.
    - Si toutes les sorties suivent la logique booléenne attendue, le système est considéré comme fiable.

### Exemple :

Considérons **2 câbles** (`C1` et `C2`) et **1 connexion** entre eux :
- Les **entrées booléennes** des câbles sont : `input1` et `input2`.

#### Logique :

1. Sorties pour le **câble supérieur (C1)** :
   **C1_output = input1 OR input2**  
   (Cela utilise la logique booléenne `OR`).

2. Sorties pour le **câble inférieur (C2)** :
   **C2_output = input1 AND input2**  
   (Cela utilise la logique booléenne `AND`).
#### Truth Table:
Pour valider la fiabilité, vous pouvez créer une table de vérité avec toutes les entrées possibles du système et vérifier si les sorties correspondent au comportement attendu.

| `input1` | `input2` | `C1_output` (OR) | `C2_output` (AND) |
| --- | --- | --- | --- |
| 0 | 0 | 0 | 0 |
| 0 | 1 | 1 | 0 |
| 1 | 0 | 1 | 0 |
| 1 | 1 | 1 | 1 |
- Si le système produit ces sorties de manière fiable pour chaque condition d'entrée, il est considéré comme **fonctionnel et fiable**.


### Exemple de Tableau de vérité dynamique (Entrées -> Sorties attendues) pour un câblage avec 6 câbles (C=6) (/!\ non vérifiée, peut contenir des erreur) :

| Entrées                  | Sorties attendues        |
|--------------------------|--------------------------|
| (0, 0, 0, 0, 0, 0)       | [0, 0, 0, 0, 0, 0]       |
| (0, 0, 0, 0, 0, 1)       | [1, 0, 0, 0, 0, 0]       |
| (0, 0, 0, 0, 1, 0)       | [1, 0, 0, 0, 0, 0]       |
| (0, 0, 0, 0, 1, 1)       | [1, 1, 0, 0, 0, 0]       |
| (0, 0, 0, 1, 0, 0)       | [1, 0, 0, 0, 0, 0]       |
| (0, 0, 0, 1, 0, 1)       | [1, 1, 0, 0, 0, 0]       |
| (0, 0, 0, 1, 1, 0)       | [1, 1, 0, 0, 0, 0]       |
| (0, 0, 0, 1, 1, 1)       | [1, 1, 1, 0, 0, 0]       |
| (0, 0, 1, 0, 0, 0)       | [1, 0, 0, 0, 0, 0]       |
| (0, 0, 1, 0, 0, 1)       | [1, 1, 0, 0, 0, 0]       |
| (0, 0, 1, 0, 1, 0)       | [1, 1, 0, 0, 0, 0]       |
| (0, 0, 1, 0, 1, 1)       | [1, 1, 1, 0, 0, 0]       |
| (0, 0, 1, 1, 0, 0)       | [1, 1, 0, 0, 0, 0]       |
| (0, 0, 1, 1, 0, 1)       | [1, 1, 1, 0, 0, 0]       |
| (0, 0, 1, 1, 1, 0)       | [1, 1, 1, 0, 0, 0]       |
| (0, 0, 1, 1, 1, 1)       | [1, 1, 1, 1, 0, 0]       |
| (0, 1, 0, 0, 0, 0)       | [1, 0, 0, 0, 0, 0]       |
| (0, 1, 0, 0, 0, 1)       | [1, 1, 0, 0, 0, 0]       |
| (0, 1, 0, 0, 1, 0)       | [1, 1, 0, 0, 0, 0]       |
| (0, 1, 0, 0, 1, 1)       | [1, 1, 1, 0, 0, 0]       |
| (0, 1, 0, 1, 0, 0)       | [1, 1, 0, 0, 0, 0]       |
| (0, 1, 0, 1, 0, 1)       | [1, 1, 1, 0, 0, 0]       |
| (0, 1, 0, 1, 1, 0)       | [1, 1, 1, 0, 0, 0]       |
| (0, 1, 0, 1, 1, 1)       | [1, 1, 1, 1, 0, 0]       |
| (0, 1, 1, 0, 0, 0)       | [1, 1, 0, 0, 0, 0]       |
| (0, 1, 1, 0, 0, 1)       | [1, 1, 1, 0, 0, 0]       |
| (0, 1, 1, 0, 1, 0)       | [1, 1, 1, 0, 0, 0]       |
| (0, 1, 1, 0, 1, 1)       | [1, 1, 1, 1, 0, 0]       |
| (0, 1, 1, 1, 0, 0)       | [1, 1, 1, 0, 0, 0]       |
| (0, 1, 1, 1, 0, 1)       | [1, 1, 1, 1, 0, 0]       |
| (0, 1, 1, 1, 1, 0)       | [1, 1, 1, 1, 0, 0]       |
| (0, 1, 1, 1, 1, 1)       | [1, 1, 1, 1, 1, 0]       |
| (1, 0, 0, 0, 0, 0)       | [1, 0, 0, 0, 0, 0]       |
| (1, 0, 0, 0, 0, 1)       | [1, 1, 0, 0, 0, 0]       |
| (1, 0, 0, 0, 1, 0)       | [1, 1, 0, 0, 0, 0]       |
| (1, 0, 0, 0, 1, 1)       | [1, 1, 1, 0, 0, 0]       |
| (1, 0, 0, 1, 0, 0)       | [1, 1, 0, 0, 0, 0]       |
| (1, 0, 0, 1, 0, 1)       | [1, 1, 1, 0, 0, 0]       |
| (1, 0, 0, 1, 1, 0)       | [1, 1, 1, 0, 0, 0]       |
| (1, 0, 0, 1, 1, 1)       | [1, 1, 1, 1, 0, 0]       |
| (1, 0, 1, 0, 0, 0)       | [1, 1, 0, 0, 0, 0]       |
| (1, 0, 1, 0, 0, 1)       | [1, 1, 1, 0, 0, 0]       |
| (1, 0, 1, 0, 1, 0)       | [1, 1, 1, 0, 0, 0]       |
| (1, 0, 1, 0, 1, 1)       | [1, 1, 1, 1, 0, 0]       |
| (1, 0, 1, 1, 0, 0)       | [1, 1, 1, 0, 0, 0]       |
| (1, 0, 1, 1, 0, 1)       | [1, 1, 1, 1, 0, 0]       |
| (1, 0, 1, 1, 1, 0)       | [1, 1, 1, 1, 0, 0]       |
| (1, 0, 1, 1, 1, 1)       | [1, 1, 1, 1, 1, 0]       |
| (1, 1, 0, 0, 0, 0)       | [1, 1, 0, 0, 0, 0]       |
| (1, 1, 0, 0, 0, 1)       | [1, 1, 1, 0, 0, 0]       |
| (1, 1, 0, 0, 1, 0)       | [1, 1, 1, 0, 0, 0]       |
| (1, 1, 0, 0, 1, 1)       | [1, 1, 1, 1, 0, 0]       |
| (1, 1, 0, 1, 0, 0)       | [1, 1, 1, 0, 0, 0]       |
| (1, 1, 0, 1, 0, 1)       | [1, 1, 1, 1, 0, 0]       |
| (1, 1, 0, 1, 1, 0)       | [1, 1, 1, 1, 0, 0]       |
| (1, 1, 0, 1, 1, 1)       | [1, 1, 1, 1, 1, 0]       |
| (1, 1, 1, 0, 0, 0)       | [1, 1, 1, 0, 0, 0]       |
| (1, 1, 1, 0, 0, 1)       | [1, 1, 1, 1, 0, 0]       |
| (1, 1, 1, 0, 1, 0)       | [1, 1, 1, 1, 0, 0]       |
| (1, 1, 1, 0, 1, 1)       | [1, 1, 1, 1, 1, 0]       |
| (1, 1, 1, 1, 0, 0)       | [1, 1, 1, 1, 0, 0]       |
| (1, 1, 1, 1, 0, 1)       | [1, 1, 1, 1, 1, 0]       |
| (1, 1, 1, 1, 1, 0)       | [1, 1, 1, 1, 1, 0]       |
| (1, 1, 1, 1, 1, 1)       | [1, 1, 1, 1, 1, 1]       |


### Étendre le processus de test pour un système avec **`c` câbles** et **`n` connexions** :

Pour tester un système ayant `c` câbles avec un nombre variable de connexions (`n`), allant de 1 à `((c-1)c)/2` connexions possibles, nous devons :

1. **Gérer dynamiquement un nombre variable de câbles (`c`) et de connexions (`n`)** :
    - Permettre le test de configurations avec tout nombre de câbles et de connexions dans les limites définies.

2. **Tester chaque ordre possible des connexions** :
    - S'assurer que le système respecte le nombre total de câbles tout en testant **toutes les permutations possibles** de l'ordre d'application des connexions.

3. **Calculer les sorties du système via la logique booléenne** :
    - Appliquer une logique booléenne (`AND`, `OR`, etc.) pour calculer les sorties pour chaque permutation des connexions.

4. **Valider les résultats via tableau de vérité** :
    - Générer un tableau de vérité dynamique pour les `c` câbles avec toutes les combinaisons d'entrées possibles.
    - Comparer les sorties du système à ce tableau de vérité pour en valider la fiabilité.

---

### Optimisation du processus de test :

1. **Éliminer les tests au-delà de la limite maximale** :
    - Pour un système avec `c` câbles, calculer la limite maximale des connexions utiles en utilisant la formule `((c-1)c)/2`.
    - Tester uniquement les ensembles de connexions **ne dépassant pas cette limite**.

2. **Se concentrer sur le plus petit sous-ensemble fiable** :
    - Commencer les tests avec les ensembles ayant le plus petit nombre de connexions (par ex. `n = 1`).
    - Ajouter progressivement des connexions et tester jusqu'à identifier un sous-ensemble fiable.
    - Interrompre les tests lorsqu'il n'est plus nécessaire d'ajouter des connexions supplémentaires.

3. **Tester toutes les combinaisons d'entrée** :
    - Utiliser le tableau de vérité généré pour tester chaque sous-ensemble de connexions sur toutes les combinaisons possibles des entrées pour les `c` câbles.
    - Si un sous-ensemble produit de manière fiable les sorties correspondant au tableau de vérité, alors ce sous-ensemble est fiable.






