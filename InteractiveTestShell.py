from MT34 import parallel_test_all_combinations


def main():
    """
    prend les entrées utilisateur pour `num_cables`, `start_size` et `max_solutions` et exécute
    la fonction `parallel_test_all_combinations()` de MT34.py.

    """
    try:
        num_cables = int(input("Enter the number of cables (num_cables): "))
        start_size = int(input("Enter the start size (start_size): "))
        max_solutions = int(input("Enter the maximum number of solutions (max_solutions): "))

        # Verify inputs are valid
        if num_cables <= 0:
            raise ValueError("The number of cables must be greater than 0.")
        if start_size <= 0:
            raise ValueError("The start size must be greater than 0.")
        if max_solutions <= 0:
            raise ValueError("The maximum number of solutions must be greater than 0.")

        # Run the function from MT3.1.2.py
        print(f"\nRunning with num_cables={num_cables}, start_size={start_size}, max_solutions={max_solutions}...\n")
        optimal_connections = parallel_test_all_combinations(num_cables, start_size, max_solutions)

        # Display results
        if optimal_connections:
            print(f"[ End! ] {len(optimal_connections)} combinaisons de connexions fiables trouvées:")
            for idx, conn in enumerate(optimal_connections, start=1):
                print(f"Solution #{idx}:")
                for item in conn:
                    print(f"  {item}")
        else:
            print("[ End! ] Aucune combinaison de connexions fiables trouvée.")

    except ValueError as e:
        print(f"Invalid input: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()