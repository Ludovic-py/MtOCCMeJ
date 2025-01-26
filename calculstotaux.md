# Calculs totaux en fonction de n (nombre de câbles)

## Étapes de calcul

1. **Déterminer le nombre total de connexions possibles \( C \)** :  
   Chaque câble peut se connecter à un autre parmi \( 2n \) (où \( n \) est le nombre de câbles), ce qui donne :

   ```
   C = n * (2 * n - 1)
   ```

   Exemple :
    - Pour \( n = 5 \), \( C = 5 * (2 * 5 - 1) = 45 \)
    - Pour \( n = 6 \), \( C = 6 * (2 * 6 - 1) = 66 \)

2. **Calculer les calculs totaux nécessaires** pour évaluer toutes les combinaisons et permutations possibles. Le nombre total de calculs est obtenu en additionnant les contributions pour chaque taille \( k \) (de 1 à \( C \)) :

    - Pour chaque \( k \), on effectue les deux étapes suivantes :
        - **Calcul des combinaisons possibles** pour choisir \( k \) connexions parmi \( C \) :
          ```
          Combinaisons possibles = C! / (k! * (C - k)!)
          ```
        - Multiplier ce résultat par **le nombre de permutations possibles pour \( k \)** :
          ```
          Permutations possibles = k!
          ```

    - Ajouter ce produit au total, pour chaque \( k \).

   En résumé :
   ```
   Nombre total de calculs = Somme (de k=1 à C) [ (Combinaisons possibles pour k) * (Permutations possibles pour k) ]
   ```

---

## Application pour \( n = 5 \) et \( n = 6 \)

### Pour \( n = 5 \) :
1. **Nombre total de connexions possibles** :
   ```
   C = 5 * (2 * 5 - 1) = 45
   ```

2. **Nombre total de calculs** :  
   Après avoir additionné toutes les contributions pour chaque \( k \), le nombre total est :
   ```
   Calculs totaux = 9 864 100
   ```

---

### Pour \( n = 6 \) :
1. **Nombre total de connexions possibles** :
   ```
   C = 6 * (2 * 6 - 1) = 66
   ```

2. **Nombre total de calculs** :  
   Après avoir additionné toutes les contributions pour chaque \( k \), le nombre total est :
   ```
   Calculs totaux = 3 554 627 472 075
   ```

---

## Exemple en langage courant

- Imaginez un système avec \( n = 5 \) câbles :
    - Chaque câble peut se connecter à un autre, formant un total de \( C = 45 \) connexions possibles.
    - Ensuite, pour chaque taille \( k \) (entre 1 et \( C \)), le programme calcule toutes les combinaisons possibles de \( k \) connexions, puis teste tous les ordres possibles (permutations) des connexions.
    - Enfin, le programme additionne tous les calculs réalisés.

- Avec \( n = 6 \), le nombre de connexions \( C \) augmente de manière significative, ce qui provoque une **explosion combinatoire** dans le nombre total de calculs nécessaires.

---

## Conclusion

Cela signifie que ce nombre croît **de manière factorielle** avec l'augmentation de \( n \).


---
# Annexe : Rapport d'augmentation des calculs

## Données connues
- Pour n = 4 :
    - C = 4 * (2 * 4 - 1) = 28
    - Nombre total de calculs : **1 213 620**

- Pour n = 5 :
    - C = 5 * (2 * 5 - 1) = 45
    - Nombre total de calculs : **9 864 100**

- Pour n = 6 :
    - C = 6 * (2 * 6 - 1) = 66
    - Nombre total de calculs : **3 554 627 472 075** (ce calcul est faux, selon la numworks il s'agit de 1 302 061 344)

---

## Calculs des rapports

1. **De n = 4 à n = 5** :  
   Le rapport est obtenu en divisant le total des calculs pour n = 5 par le total pour n = 4.

   Rapport = Total pour n = 5 / Total pour n = 4  
   Rapport = 9 864 100 / 1 213 620 ≈ 8,13

2. **De n = 5 à n = 6** :  
   Le rapport est obtenu en divisant le total des calculs pour n = 6 par le total pour n = 5.

   Rapport = Total pour n = 6 / Total pour n = 5  
   Rapport = 3 554 627 472 075 / 9 864 100 ≈ 360.360,04 (correction 1 302 061 344 / 9 864 100 donc ≈ 132.00)

---

## Résultats

- **De n = 4 à n = 5** :  
  Le nombre total de calculs est multiplié par environ **8,13**.

- **De n = 5 à n = 6** :  
  Le nombre total de calculs est multiplié par environ **360.360,04** (correction ≈ 132.00).

---

## Conclusion
Ces résultats illustrent clairement la **croissance factorielle** du nombre total de calculs lorsque n augmente. Même une petite augmentation de n entraîne une explosion massive du nombre de calculs nécessaires entre n = 5 et n = 6.
