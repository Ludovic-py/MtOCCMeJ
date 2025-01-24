from itertools import combinations, permutations
from multiprocessing import Pool, cpu_count
from T3 import boolean_calculations, verify_reliability


#import pstats
#import cProfile #pour tester l'efficacitée du programme uncomment les 2 lignes


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


def test_subset(args):
    num_cables, subset = args  # j'extrait les arguments
    for permuted_subset in permutations(subset):
        truth_table = boolean_calculations(num_cables, permuted_subset)
        if verify_reliability(truth_table):
            return permuted_subset  # solution trouvé
    return None  # Aucune solution /!\(pour ce subset)


def parallel_test_all_combinations(num_cables, start_size):      #remplace le test_all_combinations, en utilissant un pool qui se genère en fonction du nombre de coeur du processeur et alloue chaque sous ensemble de façon equilibré
    print(f"[ Launch ] Testing for {num_cables} cables, starting from {start_size} connections")

    all_possible_connections = generate_all_connections(num_cables)

    for connection_set_size in range(start_size, len(all_possible_connections) + 1):
        print(f"[ Update ] Testing combination subsets of size {connection_set_size}...")

        subsets = list(combinations(all_possible_connections, connection_set_size))

        # Création d'un pool de processus avec le nombre de CPU disponibles
        with Pool(cpu_count()) as pool:
            # Mapper les sous-ensembles aux processus
            results = pool.map(test_subset, [(num_cables, subset) for subset in subsets]) # à tester pour + eficience param: chunksize, c'est le nombre de sous ensembles à traiter simultanement results = pool.map(test_subset, [(num_cables, subset) for subset in subsets], chunksize=10)

        # analyse result pour trouver 1 solution
        for result in results:
            if result is not None:
                return result

    return None  # Aucune solution








### paramètres du programme ###


if __name__ == "__main__":
    #profiler = cProfile.Profile()
    #profiler.enable() #pour tester l'efficacitée du programme uncomment les 2 lignes


    num_cables = 4 # nombre de cables
    start_size = 1 # nombre tuples de connection à partir duquel le programme commence à chercher (ex: il est evident que pour 5 cables, il ne sufit pas de 5 cables donc on peut commencer à 6 pour economiser un nombre consequent de calculs)


    optimal_connections = parallel_test_all_combinations(num_cables, start_size)

    if optimal_connections:
        print("/!\ Combinaison de connexions fiables trouvée:")
        for conn in optimal_connections:
            print(conn)
    else:
        print("/!\ Aucune combinaison de connexions fiables trouvée.")



    #profiler.disable()                      #pour tester l'efficacitée du programme uncomment les 5 lignes
    #stats = pstats.Stats(profiler)
    #stats.strip_dirs()
    #stats.sort_stats('cumtime')
    #stats.print_stats(12)  # Affiche les 10 fonctions les plus coûteuses