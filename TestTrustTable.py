from itertools import product


def boolean_calculations(num_cables, connections):
    """
    Test the reliability of a system of cables using boolean logic.

    :param num_cables: Number of cables in the system.
    :param connections: List of connections as tuples (input1, input2, upper_func, lower_func).
                        Example: [(1, 2, "OR", "AND")] means input1 and input2 affect two cables:
                        - Upper cable applies OR
                        - Lower cable applies AND
    :return: Truth table with inputs and outputs for all cables.
    """

    def apply_logic(input1, input2, logic_func):
        """Helper function to apply boolean logic."""
        if logic_func == "OR":
            return input1 or input2
        elif logic_func == "AND":
            return input1 and input2
        elif logic_func == "XOR":
            return input1 ^ input2
        elif logic_func == "NAND":
            return not (input1 and input2)

    # Generate all possible boolean inputs for the cables
    inputs = list(product([0, 1], repeat=num_cables))

    # Truth table results
    truth_table = []

    for input_combination in inputs:
        cable_outputs = [None] * num_cables

        for conn in connections:
            input1, input2, upper_func, lower_func = conn

            # Inputs to the current connection
            input1_val = input_combination[input1 - 1]  # Cable index is 1-based
            input2_val = input_combination[input2 - 1]

            # Calculate outputs
            upper_output = apply_logic(input1_val, input2_val, upper_func)
            lower_output = apply_logic(input1_val, input2_val, lower_func)

            # Assign outputs to cables
            cable_outputs[input1 - 1] = upper_output
            cable_outputs[input2 - 1] = lower_output

        # Store the input/output pair for the truth table
        truth_table.append((input_combination, cable_outputs))

    return truth_table


# Example Usage: 2 Cables, 1 Connection
num_cables = 2
connections = [
    (1, 2, "OR", "AND")  # Connection from cable 1 to cable 2 with OR/AND rules
]

truth_table = boolean_calculations(num_cables, connections)
print("Truth Table (Inputs -> Outputs):")

for inputs, outputs in truth_table:
    print(f"Inputs: {inputs} -> Outputs: {outputs}")
