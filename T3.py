from itertools import product, combinations
# edit:  je crois qu'il y a plus besoin de combination mais flème de verifier

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

    Paramètres :
        num_cables (int) : Nombre de câbles.
        connections (list) : Liste de tuples représentant les connexions de câbles.
                             Format : (cable1, cable2, upper_logic, lower_logic)

    Renvoie :
        list : truth_table des entrées et des sorties résultantes.

    """


    # tte les input combinations
    inputs = list(product([0, 1], repeat=num_cables))
    truth_table = []

    # verifie chaque combinaison d'input
    for input_combination in inputs:
        cable_outputs = list(input_combination)  # Start with the initial input combination
        print(f"\nInitial Inputs: {input_combination}")

        # verifie les connexions de cables étape/étape+1
        for step, conn in enumerate(connections):
            input1, input2, upper_func, lower_func = conn

            # recup les valeurs actuelles des sorties de cables mises à jour
            input1_val = cable_outputs[input1]
            input2_val = cable_outputs[input2]

            # calcul fleme d'expliquer
            upper_output = apply_logic(input1_val, input2_val, upper_func)
            lower_output = apply_logic(input1_val, input2_val, lower_func)

            # Débogage : affiche les sorties de cables mises à jour et calculs(super utile)(à uncoment pour debug)
            """
            print(
                f"Step {step + 1}: Connection ({input1}, {input2}) with logic (Upper: {upper_func}, Lower: {lower_func})"
            )
            print(
                f"    - Inputs: {input1_val} (Cable {input1}), {input2_val} (Cable {input2}) => "
                f"Upper Output: {upper_output}, Lower Output: {lower_output}"
            )
            """
            # Mettre à jour les états des cables dynamiquement pour les calculs intermédiaires
            cable_outputs[input1] = upper_output
            cable_outputs[input2] = lower_output

            # Débogage : affiche les sorties de câbles mises à jour (super utile)(à uncoment pour debug)
            ##print(f"    - Updated Outputs: {cable_outputs}")

        # Ajouter les sorties finales pour cette combinaison d'entrées
        truth_table.append((input_combination, cable_outputs.copy()))  # Ajouter une copie pour éviter la modification(ou l'overwrite plutot)

    return truth_table


def is_ordered_descending(output):
    """
    Vérifier si la liste de sorties (output) est dans un ordre binaire décroissant (par exemple, [1, 1, 0, 0]).

    Paramètres :
        output (list) : Liste des valeurs de sortie.

    Renvoie :
        bool : True si ordonné, False sinon.
    """

    return output == sorted(output, reverse=True)


def verify_reliability(truth_table):
    """
    Vérifier si le système de câblage est fiable en vérifiant toutes les sorties.

    Paramètres :
        truth_table (list) : La table de vérité avec les entrées et les sorties.

    Renvoie :
        bool : True si toutes les sorties sont ordonnées de manière décroissante, False sinon.
    """

    for inputs, outputs in truth_table:
        if not is_ordered_descending(outputs):
            print(f"cablage non-fiable: Inputs: {inputs} -> Outputs: {outputs}")
            return False
    return True


# Param du programme
if __name__ == "__main__":
    # Nbr cables
    num_cables = 4

    # definir les connections: (cable1, cable2, upper_logic, lower_logic)
    # Les indices sont 0-based pour les connexions ex: le cable du haut est 0 et celui du dessous est 1
    connections = [
        (0, 2, "OR", "AND"),
        (1, 3, "OR", "AND"),
        (0, 1, "OR", "AND"),
        (2, 3, "OR", "AND"),
        (1, 2, "OR", "AND"),
    ]

    # Génère les truth table
    truth_table = boolean_calculations(num_cables, connections)
    print("\nTruth Table (Inputs -> Outputs):")

    for inputs, outputs in truth_table:
        print(f"Inputs: {inputs} -> Outputs: {outputs}")

    # verification de la fiabilitée
    if verify_reliability(truth_table):
        print("\ncablage fiable.")
    else:
        print("\ncablage pas fiable.")