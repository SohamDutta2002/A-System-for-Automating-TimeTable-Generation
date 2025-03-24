import sys
import os

# Ensure src is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Import all algorithm modules
from src.basic_algorithm_implementations import (
    hybrid_algorithm,
    genetic_algorithms,
    simulated_annealing,
    constraint_programming,
    utils
)

# Execute functions from each module (assuming each has a main function)
if __name__ == "__main__":
    print("Running Hybrid Algorithm...")
    hybrid_algorithm.main()  # Change this to the actual function name

    print("Running Genetic Algorithm...")
    genetic_algorithms.main()

    print("Running Simulated Annealing...")
    simulated_annealing.main()

    print("Running Constraint Programming...")
    constraint_programming.main()

    print("Running Utils (if applicable)...")
    utils.main()
