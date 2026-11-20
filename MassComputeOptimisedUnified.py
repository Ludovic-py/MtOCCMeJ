import multiprocessing
from functools import lru_cache
from itertools import combinations, islice, permutations, product
from multiprocessing import Pool, cpu_count

_DESCENDING_BITMASKS_CACHE = {}


def _get_descending_bitmasks(num_cables: int) -> frozenset[int]:
    """Precompute bitmasks of all binary vectors sorted in descending order."""
    cached = _DESCENDING_BITMASKS_CACHE.get(num_cables)
    if cached is not None:
        return cached

    masks = {((1 << k) - 1) << (num_cables - k) for k in range(num_cables + 1)}
    frozen = frozenset(masks)
    _DESCENDING_BITMASKS_CACHE[num_cables] = frozen
    return frozen


def _apply_logic_mask(mask1: int, mask2: int, logic_func: str, all_ones_mask: int) -> int:
    if logic_func == "OR":
        return mask1 | mask2
    if logic_func == "AND":
        return mask1 & mask2
    if logic_func == "XOR":
        return mask1 ^ mask2
    if logic_func == "NAND":
        return (mask1 & mask2) ^ all_ones_mask
    raise ValueError(f"logique non suportée: {logic_func}")


@lru_cache(maxsize=None)
def _initial_wire_masks(num_cables: int) -> tuple[int, ...]:
    """
    For cable index c in [0, num_cables - 1], bit i (from MSB to LSB across 2^num_cables
    combinations in product([0, 1], repeat=num_cables)) holds input c for combination i.
    """
    total_combos = 1 << num_cables
    masks = []
    for cable_idx in range(num_cables):
        shift = num_cables - 1 - cable_idx
        mask = 0
        for combo_idx in range(total_combos):
            if (combo_idx >> shift) & 1:
                mask |= 1 << (total_combos - 1 - combo_idx)
        masks.append(mask)
    return tuple(masks)


def apply_logic(input1, input2, logic_func):
    """
    Fonction helper pour appliquer la logique booléenne.
    prends en charge : OR, AND, XOR, NAND.
    """
    if logic_func == "OR":
        return input1 or input2
    elif logic_func == "AND":
        return input1 and input2
    elif logic_func == "XOR":
        return input1 ^ input2
    elif logic_func == "NAND":
        return not (input1 and input2)
    else:
        raise ValueError(f"logique non suportée: {logic_func}")


def boolean_calculations(num_cables, connections):
    """
    Générer table de vérité basée sur num_cable et connexions.
    """
    total_combos = 1 << num_cables
    all_ones_mask = (1 << total_combos) - 1
    wire_masks = list(_initial_wire_masks(num_cables))

    for input1, input2, upper_func, lower_func in connections:
        m1 = wire_masks[input1]
        m2 = wire_masks[input2]
        wire_masks[input1] = _apply_logic_mask(m1, m2, upper_func, all_ones_mask)
        wire_masks[input2] = _apply_logic_mask(m1, m2, lower_func, all_ones_mask)

    inputs = list(product([0, 1], repeat=num_cables))
    truth_table = []
    for combo_idx, input_combination in enumerate(inputs):
        bit_pos = total_combos - 1 - combo_idx
        outputs = [(wire_masks[c] >> bit_pos) & 1 for c in range(num_cables)]
        truth_table.append((input_combination, outputs))

    return truth_table


def is_ordered_descending(output):
    """
    Vérifier si la liste de sorties (output) est dans un ordre binaire décroissant (par exemple, [1, 1, 0, 0]).
    """
    return output == sorted(output, reverse=True)


def verify_reliability(truth_table):
    """
    Vérifier si le système de câblage est fiable en vérifiant toutes les sorties.
    """
    if not truth_table:
        return True

    num_cables = len(truth_table[0][1])
    valid_masks = _get_descending_bitmasks(num_cables)

    for _, outputs in truth_table:
        out_mask = 0
        for val in outputs:
            out_mask = (out_mask << 1) | (1 if val else 0)
        if out_mask not in valid_masks:
            return False
    return True


def generate_all_connections(num_cables):
    """
    Genere toutes connexions possibles pour les câbles en utilisant uniquement "OR" (supérieur)
    et "AND" (inférieur) pour chaque connexion.
    Chaque connexion = (input1, input2, "OR", "AND").
    """
    return [
        (input1, input2, "OR", "AND")
        for input1, input2 in combinations(range(num_cables), 2)
    ]


def _is_permutation_reliable(num_cables, permuted_subset, init_masks, all_ones_mask, valid_masks):
    wire_masks = list(init_masks)
    for input1, input2, upper_func, lower_func in permuted_subset:
        m1 = wire_masks[input1]
        m2 = wire_masks[input2]
        wire_masks[input1] = _apply_logic_mask(m1, m2, upper_func, all_ones_mask)
        wire_masks[input2] = _apply_logic_mask(m1, m2, lower_func, all_ones_mask)

    total_combos = 1 << num_cables
    for bit_pos in range(total_combos):
        out_mask = 0
        for c in range(num_cables):
            out_mask = (out_mask << 1) | ((wire_masks[c] >> bit_pos) & 1)
        if out_mask not in valid_masks:
            return False
    return True


def test_subset(args):
    num_cables, subset = args
    total_combos = 1 << num_cables
    all_ones_mask = (1 << total_combos) - 1
    init_masks = _initial_wire_masks(num_cables)
    valid_masks = _get_descending_bitmasks(num_cables)

    solutions = []
    for permuted_subset in permutations(subset):
        if _is_permutation_reliable(
            num_cables, permuted_subset, init_masks, all_ones_mask, valid_masks
        ):
            solutions.append(permuted_subset)
    return solutions


def _batched_subsets(all_possible_connections, connection_set_size, batch_size):
    iterator = combinations(all_possible_connections, connection_set_size)
    while True:
        batch = list(islice(iterator, batch_size))
        if not batch:
            break
        yield batch


def parallel_test_all_combinations(num_cables, start_size, max_solutions):
    """
    Recherche les cablages fiables en parallèle et retourne les max_solutions premières solutions trouvées.
    """
    print(f"[ Launch ] Testing for {num_cables} cables, starting from {start_size} connections")

    all_possible_connections = generate_all_connections(num_cables)
    solutions = []
    workers = cpu_count() or 1
    batch_size = max(workers * 8, 32)

    with Pool(workers) as pool:
        for connection_set_size in range(start_size, len(all_possible_connections) + 1):
            print(f"[ Update ] Testing combination subsets of size {connection_set_size}...")

            for batch in _batched_subsets(all_possible_connections, connection_set_size, batch_size):
                tasks = [(num_cables, subset) for subset in batch]
                for result in pool.imap_unordered(test_subset, tasks, chunksize=8):
                    if result:
                        solutions.extend(result)
                        if len(solutions) >= max_solutions:
                            return solutions[:max_solutions]

    return solutions


if __name__ == "__main__":
    multiprocessing.set_start_method("spawn", force=True)

    # Mode de lancement : "search" (recherche parallèle) ou "verify" (test d'un câblage précis)
    MODE = "search"

    if MODE == "verify":
        num_cables = 5
        connections = [
            (0, 2, "OR", "AND"),
            (1, 3, "OR", "AND"),
            (0, 1, "OR", "AND"),
            (2, 3, "OR", "AND"),
            (1, 2, "OR", "AND"),
        ]

        truth_table = boolean_calculations(num_cables, connections)
        print("\nTruth Table (Inputs -> Outputs):")

        for inputs, outputs in truth_table:
            print(f"Inputs: {inputs} -> Outputs: {outputs}")

        if verify_reliability(truth_table):
            print("\ncablage fiable.")
        else:
            print("\ncablage pas fiable.")

    elif MODE == "search":
        num_cables = 4
        start_size = 1
        max_solutions = 3

        optimal_connections = parallel_test_all_combinations(num_cables, start_size, max_solutions)

        if optimal_connections:
            print(f"[  End!  ] ({len(optimal_connections)}/{max_solutions}) combinaisons de connexions fiables trouvées:")
            for idx, conn in enumerate(optimal_connections, start=1):
                print(f"Solution #{idx}:")
                for item in conn:
                    print(f"  {item}")
        else:
            print("[  End!  ] Aucune combinaison de connexions fiables trouvée.")
