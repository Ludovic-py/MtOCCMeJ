from itertools import combinations
from cable_v4_1 import MainWindow  # Import MainWindow from cable_v4.1


def generate_possible_connections(n):
    """
    Generate all possible connections (pairs) between n cables.

    Args:
        n (int): Number of cables.

    Returns:
        list: A list of all possible unique connections.
    """
    # Generate all pairs (1, 2), (1, 3), ..., (n-1, n)
    return list(combinations(range(1, n + 1), 2))


def test_all_combinations(n):
    """
    Test all possible subsets of connections for n cables using the boolean reliability test.

    Args:
        n (int): Number of cables.

    Returns:
        None
    """
    # Step 1: Generate all possible connections
    possible_connections = generate_possible_connections(n)
    print(f"Possible connections for {n} cables: {possible_connections}\n")

    # Step 2: Initialize an instance of MainWindow (from cable_v4.1)
    cable_system = MainWindow()
    cable_system.nbcable = n  # Set the number of cables
    cable_system.commencer()  # Reinitialize the system with the correct setup

    # Step 3: Generate all subsets of possible connections
    for r in range(1, len(possible_connections) + 1):  # Subset sizes
        subsets = combinations(possible_connections, r)

        for subset in subsets:
            print(f"Testing combination: {subset}")

            # Step 4: Set the links in the cable system for the current subset
            set_links_in_system(cable_system, subset)

            # Step 5: Test the subset via the reliability check
            is_reliable = cable_system.est_fiable()
            print(f"  Result: {'Reliable' if is_reliable else 'Unreliable'}\n")


def set_links_in_system(cable_system, subset):
    """
    Configure the cable system (MainWindow) with the given connection subset.

    Args:
        cable_system (MainWindow): The cable system instance.
        subset (tuple): A subset of connections to configure as links.
    """
    # Reset all links
    cable_system.listLien = []  # Reset the list of links

    # Add each connection in the subset as a link in the cable system
    for connection in subset:
        y1, y2 = connection
        cable_system.creer_lien(0, y1 - 1)  # Create link at adjusted index (0-based)
        cable_system.creer_lien(0, y2 - 1)  # Create link at adjusted index (0-based)

    # Update the system to reflect changes
    cable_system.actualiser()


# Example usage with 4 cables
test_all_combinations(4)