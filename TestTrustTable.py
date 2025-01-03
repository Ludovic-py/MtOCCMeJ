from itertools import product

# système de verification

def is_ordered_descending(output):
    """
    Vérifie si les valeurs de la sortie sont en ordre décroissant
    les 1 avant les 0, comme [1, 1, 1, 0] (pour une ligne)

     output: Liste des valeurs de sortie (exemple : [1, 1, 1, 0]).
    return True si la sortie est en ordre décroissant, False sinon.
    """
    return output == sorted(output, reverse=True)


def verify_reliability(truth_table):
    """
    Vérifie si le câblage est fiable en s'assurant que toutes les sorties sont ordonnées.
    Une sortie est valide uniquement si elle est en ordre décroissant

    truth_table: Table de vérité contenant les entrées et sorties pour chaque combinaison.
    return: True si le câblage est fiable, False sinon.
    """
    for inputs, outputs in truth_table:
        if not is_ordered_descending(outputs):  # Vérifier si une sortie est invalide
            print(f"Câblage invalide : Inputs: {inputs} -> Outputs: {outputs}")
            return False
    return True



#reste du programme

def boolean_calculations(num_cables, connections):
    """
    meme que l'autre marche pas totalement et moitié foireux pas touche je changerai plus tard

    nesamoins celui qui à le plus de potentiel des deux
    """

    def apply_logic(input1, input2, logic_func):
        """fonction helper pour mettre logic boolean"""
        if logic_func == "OR":
            return input1 or input2
        elif logic_func == "AND":
            return input1 and input2
        elif logic_func == "XOR":
            return input1 ^ input2
        elif logic_func == "NAND":
            return not (input1 and input2)

    inputs = list(product([0, 1], repeat=num_cables))

    truth_table = []

    for input_combination in inputs:
        cable_outputs = [None] * num_cables

        for conn in connections:
            input1, input2, upper_func, lower_func = conn

            
            input1_val = input_combination[input1 - 1]  #  index du cable is basé 1
            input2_val = input_combination[input2 - 1]

            # calcule output
            upper_output = apply_logic(input1_val, input2_val, upper_func)
            lower_output = apply_logic(input1_val, input2_val, lower_func)

            # assigne les outpu faits juste avant
            cable_outputs[input1 - 1] = upper_output
            cable_outputs[input2 - 1] = lower_output

        # enregistre input ouput pour la paire
        truth_table.append((input_combination, cable_outputs))

    return truth_table

# SECTION DE SELECTION DES PARAMETRE DU PROGRAMME
# Exemple utilisation : 4 Cables, 12 Connection


# Nombre de câbles dans le système
num_cables = 4

# --Liste des connexions entre les câbles--
# Chaque connexion est définie par un tuple (câble1, câble2, fonction_supérieure, fonction_inférieure)
# câble1 et câble2 représentent les indices des câbles connectés
# fonction_supérieure applique une opération logique sur la sortie supérieure ici "OR" mais peut être modifiée
# fonction_inférieure applique une opération logique sur la sortie inférieure ici "AND" /idem/

# IMPORTANT dans ma representation, le cable 1 part du dessus donc les cables suivants sont en desous

connections = [
    (1, 2, "OR", "AND"),  # Connexion entre le câble 1 et le câble 2
    (1, 3, "OR", "AND"),  # Connexion entre le câble 1 et le câble 3
    (1, 4, "OR", "AND"),  # Connexion entre le câble 1 et le câble 4
    (2, 3, "OR", "AND"),  # Connexion entre le câble 2 et le câble 3
    (2, 4, "OR", "AND"),  # Connexion entre le câble 2 et le câble 4
    (3, 4, "OR", "AND"),  # Connexion entre le câble 3 et le câble 4
    (1, 2, "OR", "AND"),  # Deuxième connexion entre le câble 1 et le câble 2
    (2, 3, "OR", "AND"),  # Deuxième connexion entre le câble 2 et le câble 3
    (3, 4, "OR", "AND"),  # Deuxième connexion entre le câble 3 et le câble 4
    (1, 3, "OR", "AND"),  # Deuxième connexion entre le câble 1 et le câble 3
    (1, 4, "OR", "AND"),  # Deuxième connexion entre le câble 1 et le câble 4
    (2, 4, "OR", "AND"),  # Deuxième connexion entre le câble 2 et le câble 4
]

truth_table = boolean_calculations(num_cables, connections)
print("Truth Table (Inputs -> Outputs):")

for inputs, outputs in truth_table:
    print(f"Inputs: {inputs} -> Outputs: {outputs}")


# Vérification de la fiabilité

if verify_reliability(truth_table):
    print("Câblage fiable")
else:
    print("Câblage non fiable")


