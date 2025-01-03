from itertools import product


def boolean_calculations(num_cables, connections):
    """
    meme que l'autre
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


# Exemple utilisation : 2 Cables, 1 Connection
num_cables = 2
connections = [
    (1, 2, "OR", "AND")  # connection de cable 1 au 2eme avec regle OR/AND
]

truth_table = boolean_calculations(num_cables, connections)
print("Truth Table (Inputs -> Outputs):")

for inputs, outputs in truth_table:
    print(f"Inputs: {inputs} -> Outputs: {outputs}")
