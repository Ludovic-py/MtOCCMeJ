from itertools import combinations
from TestTrustTable import boolean_calculations, verify_reliability


def generate_all_connections(num_cables:int):
    """Genere toutes connexions possibles pour les câbles en utilisant uniquement "OR" (supérieur)
    et "AND" (inférieur) pour chaque connexion.
    Chaque connexion = (input1, input2, "OR", "AND").
    :param num_cables nombre de cables
    """

    all_connections = []

    # genere des combinaison de 2 cable pour faire les differante connections
    for input1, input2 in combinations(range(1, num_cables + 1), 2):
        # mettre que "OR" et "AND" respectivement superieur et inferieur
        all_connections.append((input1, input2, "OR", "AND"))

    return all_connections


def test_all_combinations(num_cables:int):
    """teste toute les cobinaison de connection possibles pour trouver la plus petite
    qui est fiable en utilisant que les mode "OR", "AND".
    :param num_cables nombre de cables
    """
    all_possible_connections = generate_all_connections(num_cables)

    # augmente le nombre de connection du set par 1, en commencant par 1
    for connection_set_size in range(1, len(all_possible_connections) + 1):
        print(f"Testing combination sets of size {connection_set_size}...")

        # test tout les sets de la taille actuelle (le problème est là, moi vivre vouloir non)
        for subset in combinations(all_possible_connections, connection_set_size):
            truth_table = boolean_calculations(num_cables, subset)
            if verify_reliability(truth_table):
                # revoie le premier set de connection qui fonctionne
                return subset
    return None  # aucune solution trouvée

# SECTION PARAMETRE DU PROGRAMME


if __name__ == "__main__":
    num_cables = 6
    optimal_connections = test_all_combinations(num_cables)

    if optimal_connections:
        print("Combinaison de connections fiables trouvée:")
        for conn in optimal_connections:
            print(conn)
    else:
        print("Aucune combinaison de connections fiables trouvée:")
