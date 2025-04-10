'''
# main.py
import argparse
import logging
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import data ingestion components
from src.data_ingestion_process.data_loader import DataLoader
from src.data_ingestion_process.data_validator import DataValidator
from src.data_ingestion_process.data_transformer import DataTransformer

# Import algorithm components
from src.hybrid_algorithm import HybridAlgorithm
from src.genetic_algorithms import GeneticAlgorithm
from src.simulated_annealing import SimulatedAnnealing
from src.constraint_programming import ConstraintProgramming

def main():
    """Main entry point for the timetable generation system."""
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Timetable Generation System")
    parser.add_argument("input_file", help="Path to input JSON file")
    parser.add_argument("--algorithm", choices=["ga", "sa", "cp", "hybrid"], 
                      default="hybrid", help="Algorithm to use (default: hybrid)")
    parser.add_argument("--output", help="Path to output file")
    parser.add_argument("--visualize", action="store_true", help="Visualize results")
    args = parser.parse_args()
    
    # Initialize data ingestion pipeline
    loader = DataLoader()
    validator = DataValidator()
    transformer = DataTransformer()
    
    # Load and process input data
    try:
        logger.info(f"Processing input file: {args.input_file}")
        raw_data = loader.load_data(args.input_file)
        validation_result = validator.validate(raw_data)
        
        if not validation_result["is_valid"]:
            logger.error(f"Data validation failed: {validation_result['errors']}")
            return 1
            
        processed_data = transformer.transform(raw_data)
        logger.info(f"Successfully processed input data")
        
        # Select and run the algorithm
        if args.algorithm == "ga":
            logger.info("Running Genetic Algorithm")
            algorithm = GeneticAlgorithm(processed_data)
        elif args.algorithm == "sa":
            logger.info("Running Simulated Annealing")
            algorithm = SimulatedAnnealing(processed_data)
        elif args.algorithm == "cp":
            logger.info("Running Constraint Programming")
            algorithm = ConstraintProgramming(processed_data)
        else:  # hybrid
            logger.info("Running Hybrid Algorithm")
            algorithm = HybridAlgorithm(processed_data)
            
        # Execute the algorithm
        result = algorithm.run()
        
        # Save the result
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = args.output or f"data/output/timetable_{timestamp}.json"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        loader.save_data(result, output_path)
        logger.info(f"Results saved to {output_path}")
        
        # Visualize if requested
        if args.visualize:
            from src.utils import visualize_timetable
            visualize_timetable(result, processed_data)
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return 1
        
    return 0

if __name__ == "__main__":
    exit(main())
'''



'''
import argparse
import logging
from src.data_ingestion_process.data_loader import DataLoader
from src.data_ingestion_process.data_validator import DataValidator
from src.data_ingestion_process.data_transformer import DataTransformer

from src.basic_algorithm_implementations.genetic_algorithms import GeneticAlgorithm
from src.basic_algorithm_implementations.simulated_annealing import SimulatedAnnealing
from src.basic_algorithm_implementations.hybrid_algorithm import HybridAlgorithm

def main():
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Automated Timetable Generation System")
    parser.add_argument("input_file", help="Path to the input JSON file")
    parser.add_argument("--algorithm", choices=["ga", "sa", "hybrid"], default="hybrid",
                        help="Algorithm to use (default: hybrid)")
    parser.add_argument("--output", help="Path to save the output timetable")
    args = parser.parse_args()

    # Initialize data ingestion components
    loader = DataLoader()
    validator = DataValidator()
    transformer = DataTransformer()

    try:
        # Step 1: Load input data
        raw_data = loader.load_json(args.input_file)

        # Step 2: Validate input data
        validation_result = validator.validate(raw_data)
        if not validation_result["is_valid"]:
            logger.error(f"Validation errors:\n{validation_result['errors']}")
            return 1

        # Step 3: Transform input data for algorithm processing
        processed_data = transformer.transform(raw_data)

        # Step 4: Select and run the algorithm
        if args.algorithm == "ga":
            logger.info("Running Genetic Algorithm...")
            algorithm = GeneticAlgorithm(processed_data)
        elif args.algorithm == "sa":
            logger.info("Running Simulated Annealing...")
            algorithm = SimulatedAnnealing(processed_data)
        elif args.algorithm == "hybrid":
            logger.info("Running Hybrid Algorithm...")
            algorithm = HybridAlgorithm(processed_data)
        else:
            raise ValueError(f"Unsupported algorithm: {args.algorithm}")

        result = algorithm.run()

        # Step 5: Save the result to a file or print it out
        output_path = args.output or "data/output/timetable_output.json"
        loader.save_data(result, output_path)
        logger.info(f"Timetable saved to {output_path}")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return 1

if __name__ == "__main__":
    main()
'''

import random
import math

# Constants
POPULATION_SIZE = 300
NUM_GENERATIONS = 500
MUTATION_RATE = 0.2
CROSSOVER_RATE = 0.8
INITIAL_TEMP = 1000
FINAL_TEMP = 1
COOLING_RATE = 0.99
MAX_ITER = 100

# Problem parameters
teachers = ["T1", "T2", "T3", "T4", "T5", "T6"]
courses = ["C1", "C2", "C3", "C4", "C5"]
rooms = ["R1", "R2", "R3", "R4"]
timeslots = [0, 1, 2, 3, 4]


def generate_timetable():
    timetable = []
    for teacher in teachers:
        teacher_schedule = []
        for course in courses:
            timeslot = random.choice(timeslots)
            room = random.choice(rooms)
            teacher_schedule.append((timeslot, room))
        timetable.append(teacher_schedule)
    return timetable


def crossover(parent1, parent2):
    child1 = []
    child2 = []
    for t1, t2 in zip(parent1, parent2):
        crossover_point = random.randint(1, len(t1) - 1)
        child1.append(t1[:crossover_point] + t2[crossover_point:])
        child2.append(t2[:crossover_point] + t1[crossover_point:])
    return child1, child2


def mutate(timetable):
    for teacher_schedule in timetable:
        if random.random() < MUTATION_RATE:
            i, j = random.sample(range(len(teacher_schedule)), 2)
            teacher_schedule[i], teacher_schedule[j] = teacher_schedule[j], teacher_schedule[i]


def acceptance_probability(delta_fitness, temperature):
    if delta_fitness > 0:
        return 1.0
    return math.exp(delta_fitness / temperature)


def mutate_timetable(timetable):
    new_timetable = [teacher_schedule[:] for teacher_schedule in timetable]
    mutate(new_timetable)
    return new_timetable


def simulated_annealing(timetable):
    current_temp = INITIAL_TEMP
    best_timetable = timetable[:]
    current_timetable = timetable[:]
    best_fitness = fitness(timetable)

    while current_temp > FINAL_TEMP:
        for _ in range(MAX_ITER):
            new_timetable = mutate_timetable(current_timetable)
            new_fitness = fitness(new_timetable)

            if new_fitness > best_fitness:
                best_timetable = new_timetable[:]
                best_fitness = new_fitness
            elif random.random() < acceptance_probability(new_fitness - best_fitness, current_temp):
                current_timetable = new_timetable[:]

        current_temp *= COOLING_RATE
    return best_timetable


def print_timetable(timetable):
    print("\nDetailed Timetable:")
    print("=" * 50)
    for teacher_idx, teacher_schedule in enumerate(timetable):
        print(f"\nTeacher {teachers[teacher_idx]} Schedule:")
        print("-" * 30)
        for course_idx, (timeslot, room) in enumerate(teacher_schedule):
            print(f"  Course {courses[course_idx]}: Timeslot {timeslot}, Room {room}")
    print("=" * 50)


def fitness(timetable):
    conflicts = 0
    room_overlaps = 0

    # Check for timeslot conflicts for each teacher
    for teacher_schedule in timetable:
        used_timeslots = set()
        for assignment in teacher_schedule:
            timeslot, room = assignment
            if timeslot in used_timeslots:
                conflicts += 1  # Conflict within the teacher's schedule
            used_timeslots.add(timeslot)

    # Check for room conflicts at the same timeslot across all teachers
    timeslot_room_assignment = {}
    for teacher_schedule in timetable:
        for assignment in teacher_schedule:
            timeslot, room = assignment
            if (timeslot, room) in timeslot_room_assignment:
                room_overlaps += 1  # Room already assigned at this timeslot
            timeslot_room_assignment[(timeslot, room)] = True

    # Penalize gaps in the timetable for each teacher
    for teacher_schedule in timetable:
        sorted_times = sorted(assignment[0] for assignment in teacher_schedule)
        for i in range(1, len(sorted_times)):
            if sorted_times[i] - sorted_times[i - 1] > 1:  # If there's a gap
                conflicts += 1

    # Calculate maximum possible conflicts
    max_possible_conflicts = (
            len(teachers) * len(courses) * (len(courses) - 1) // 2 +  # Maximum teacher conflicts
            len(timeslots) * len(rooms) * (len(teachers) - 1) // 2 +  # Maximum room conflicts
            len(teachers) * (len(timeslots) - 1)  # Maximum gaps
    )

    # Convert to positive fitness value
    # Higher fitness means fewer conflicts
    total_conflicts = conflicts + room_overlaps
    fitness_value = max_possible_conflicts - total_conflicts

    return fitness_value


def genetic_algorithm():
    # Calculate and print maximum possible fitness at the start
    max_possible_conflicts = (
            len(teachers) * len(courses) * (len(courses) - 1) // 2 +  # Maximum teacher conflicts
            len(timeslots) * len(rooms) * (len(teachers) - 1) // 2 +  # Maximum room conflicts
            len(teachers) * (len(timeslots) - 1)  # Maximum gaps
    )
    print(f"\nMaximum possible fitness value: {max_possible_conflicts}")
    print(f"Target: Minimize conflicts to achieve fitness close to {max_possible_conflicts}\n")

    population = [generate_timetable() for _ in range(POPULATION_SIZE)]
    best_fitness_so_far = float('-inf')

    for generation in range(NUM_GENERATIONS):
        population = sorted(population, key=fitness, reverse=True)
        current_best_fitness = fitness(population[0])

        # Update best fitness if we found a better solution
        if current_best_fitness > best_fitness_so_far:
            best_fitness_so_far = current_best_fitness
            print(f"\nNew best solution found at generation {generation}:")
            print(f"Fitness: {current_best_fitness}")
            print(f"Conflicts: {max_possible_conflicts - current_best_fitness}")
            print_timetable(population[0])

        next_population = population[:POPULATION_SIZE // 2]

        while len(next_population) < POPULATION_SIZE:
            parent1 = random.choice(population[:POPULATION_SIZE // 2])
            parent2 = random.choice(population[:POPULATION_SIZE // 2])
            if random.random() < CROSSOVER_RATE:
                child1, child2 = crossover(parent1, parent2)
                next_population.append(child1)
                next_population.append(child2)

        for individual in next_population:
            mutate(individual)

        population = next_population

        # Simulated Annealing for the best individual in each generation
        best_individual = population[0]
        refined_individual = simulated_annealing(best_individual)
        population[0] = refined_individual

        # Print progress every 100 generations
        if generation % 100 == 0:
            print(f"\nGeneration {generation}:")
            print(f"Current best fitness: {current_best_fitness}")
            print(f"Best fitness so far: {best_fitness_so_far}")
            print(f"Conflicts in current best: {max_possible_conflicts - current_best_fitness}")

    print("\nFinal Results:")
    print(f"Best fitness achieved: {best_fitness_so_far}")
    print(f"Total conflicts in best solution: {max_possible_conflicts - best_fitness_so_far}")
    return max(population, key=fitness)


# Main execution
if __name__ == "__main__":
    print("Starting Timetable Generation...")
    print(f"Number of Teachers: {len(teachers)}")
    print(f"Number of Courses: {len(courses)}")
    print(f"Number of Rooms: {len(rooms)}")
    print(f"Number of Timeslots: {len(timeslots)}")
    print(f"Population Size: {POPULATION_SIZE}")
    print(f"Number of Generations: {NUM_GENERATIONS}")
    print(f"Mutation Rate: {MUTATION_RATE}")
    print(f"Crossover Rate: {CROSSOVER_RATE}")
    print("\nInitializing Genetic Algorithm...")

    best_timetable = genetic_algorithm()

    print("\nFinal Best Timetable:")
    print_timetable(best_timetable)