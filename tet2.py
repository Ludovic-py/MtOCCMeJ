from itertools import combinations, product


def trouver_sous_ensemble_fiable(c, logic_funcs=("OR", "AND")):
    """
    Trouve le plus petit sous-ensemble de connexions pour 'c' câbles qui respecte le tableau de vérité dynamique.

    :param c: Nombre de câbles dans le système.
    :param logic_funcs: Tuple des fonctions logiques appliquées aux connexions, par défaut ("OR", "AND").
    :return: Le plus petit sous-ensemble fiable et le tableau de vérité dynamique attendu.
    """

    def appliquer_logique(entree1, entree2, fonction_logique):
        """Applique une fonction logique aux deux entrées."""
        if fonction_logique == "OR":
            return entree1 or entree2
        elif fonction_logique == "AND":
            return entree1 and entree2
        elif fonction_logique == "XOR":
            return entree1 ^ entree2
        elif fonction_logique == "NOR":
            return not (entree1 or entree2)
        elif fonction_logique == "NAND":
            return not (entree1 and entree2)

    # Calcul de la limite maximale des connexions possibles
    limite_connexions = (c * (c - 1)) // 2  # ((c-1)c)/2

    # Générer toutes les connexions possibles (toutes les combinaisons non-ordonnées entre câbles)
    toutes_les_connexions = list(combinations(range(1, c + 1), 2))  # Les câbles sont numérotés de 1 à c

    # Générer toutes les combinaisons d'entrées possibles (2^c)
    entrees = list(product([0, 1], repeat=c))  # Combinaisons binaires pour c câbles

    # Générer le tableau de vérité dynamique attendu
    tableau_dynamique = []
    for entree in entrees:
        nombre_actives = sum(entree)  # Compter le nombre de câbles activés (valant 1)
        # Générer une sortie avec 'nombre_actives' câbles à 1, suivis de 0
        sortie_attendue = [1] * nombre_actives + [0] * (c - nombre_actives)
        tableau_dynamique.append((entree, sortie_attendue))

    # Tester des sous-ensembles de connexions de tailles croissantes
    for taille_sous_ensemble in range(1, limite_connexions):
        # Générer tous les sous-ensembles de connexions pour cette taille
        sous_ensembles = combinations(toutes_les_connexions, taille_sous_ensemble)

        for sous_ensemble in sous_ensembles:
            # Vérifier si ce sous-ensemble est fiable
            tous_resultats_fiables = True

            for entree, sortie_attendue in tableau_dynamique:
                sorties = list(entree)  # Initialiser les sorties avec les entrées

                # Appliquer chaque connexion dans le sous-ensemble
                for connexion in sous_ensemble:
                    cable1, cable2 = connexion
                    entree1 = sorties[cable1 - 1]  # Indexé à partir de 1
                    entree2 = sorties[cable2 - 1]

                    # Appliquer les fonctions logiques (par défaut : "OR" et "AND")
                    sortie1 = appliquer_logique(entree1, entree2, logic_funcs[0])
                    sortie2 = appliquer_logique(entree1, entree2, logic_funcs[1])

                    # Mettre à jour les sorties des câbles
                    sorties[cable1 - 1] = sortie1
                    sorties[cable2 - 1] = sortie2

                # Comparer les résultats aux sorties attendues
                if sorties != sortie_attendue:
                    tous_resultats_fiables = False
                    break

            # Si ce sous-ensemble est fiable, le retourner
            if tous_resultats_fiables:
                return sous_ensemble, tableau_dynamique

    return None, tableau_dynamique  # Aucun sous-ensemble fiable trouvé


# Exemple d'utilisation
cables = 6  # Nombre de câbles
fonctions_logiques = ("OR", "AND")  # Fonctions logiques appliquées aux connexions

sous_ensemble_fiable, tableau_dynamique = trouver_sous_ensemble_fiable(cables, fonctions_logiques)

if sous_ensemble_fiable:
    print("\nPlus petit sous-ensemble fiable trouvé :")
    print(sous_ensemble_fiable)
else:
    print("\nAucun sous-ensemble fiable trouvé.")

print("\nTableau de vérité dynamique (Entrées -> Sorties attendues) :")
for ligne in tableau_dynamique:
    print(ligne)