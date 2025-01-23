from itertools import combinations, permutations
from T3 import boolean_calculations, verify_reliability


def generate_all_connections(num_cables):
    """
        Genere toutes connexions possibles pour les câbles en utilisant uniquement "OR" (supérieur)
        et "AND" (inférieur) pour chaque connexion.
        Chaque connexion = (input1, input2, "OR", "AND").
        :param num_cables nombre de cables

    """
    all_connections = []

    # Générer des combinaisons de 2 câbles pour toute les connexions différentes
    for input1, input2 in combinations(range(num_cables), 2):
        all_connections.append((input1, input2, "OR", "AND"))

    return all_connections


def test_all_combinations(num_cables,start_size=4):
    print(f"[launch] testing for {num_cables} cables, starting from {start_size} connections")
    """
        param:
            num_cables (int): nbr cables.
            start_size (int): nombre minimum de cable à partir duquel commence le prog.

        renvoie:
            tuple: première combinaison de connexions fiables trouvée, None si aucune solution n'est trouvée.
            """
    all_possible_connections = generate_all_connections(num_cables)

    # Tester des sous-ensembles de taille incrementielle
    for connection_set_size in range(start_size, len(all_possible_connections) + 1):
        print(f"[update] Testing combination subsets of size {connection_set_size}, max set size before triggering force stop: {len(all_possible_connections) + 1}...")

        # Teste tous les sous-ensembles de la taille actuelle
        for subset in combinations(all_possible_connections, connection_set_size):

            # Pour chaque sous-ensemble, tester toutes les permutations ( priorisations de merde qui est en pertie ce pourquoi ça ne marchait pas).
            for permuted_subset in permutations(subset):
                truth_table = boolean_calculations(num_cables, permuted_subset)
                if verify_reliability(truth_table):
                    # renvoie le premier set de combinaison trouvé
                    return permuted_subset
                    ##print(f"connection set size:{connection_set_size} / max set size before triggering force stop: {len(all_possible_connections) + 1}")
    return None  # trouvé r


# paramètres du programme
if __name__ == "__main__":
    num_cables = 5
    optimal_connections = test_all_combinations(num_cables)

    if optimal_connections:
        print("/!\ Combinaison de connexions fiables trouvée:")
        for conn in optimal_connections:
            print(conn)
    else:
        print("Aucune combinaison de connexions fiables trouvée.")