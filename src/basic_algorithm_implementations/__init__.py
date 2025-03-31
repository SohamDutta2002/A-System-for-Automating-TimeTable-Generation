"""
Automated Timetable Generation System

This package implements a hybrid algorithm combining Genetic Algorithms (GA), 
Simulated Annealing (SA), and Constraint Programming (CP) approaches for 
generating optimal academic timetables.

Created by: Arkaprabha Bera, Rupam Nandi, Soham Dutta, Akanksh Kumar Shaw
"""

# Version information
__version__ = '1.0.0'
__author__ = 'Arkaprabha Bera, Rupam Nandi, Soham Dutta, Akanksh Kumar Shaw'

# Import main components to make them available at package level
from .models import Teacher, Student, Course, Room, TimeSlot, StudentGroup
from .genetic_algorithms import GeneticAlgorithm
from .simulated_annealing import SimulatedAnnealing
from .constraint_programming import ConstraintProgramming
from .hybrid_algorithm import HybridAlgorithm
#from .utils import load_json_data, save_timetable, visualize_timetable


__all__ = [
    'Teacher', 'Student', 'Course', 'Room', 'TimeSlot', 'StudentGroup',
    'GeneticAlgorithm', 'SimulatedAnnealing', 'ConstraintProgramming', 'HybridAlgorithm',
    'load_json_data', 'save_timetable', 'visualize_timetable',
]

# Package-level configurations
DEFAULT_CONFIG = {
    'ga_params': {
        'population_size': 300,
        'generations': 500,
        'mutation_rate': 0.2,
        'crossover_rate': 0.8,
        'selection_method': 'tournament',
        'tournament_size': 3,
        'elitism_count': 5
    },
    'sa_params': {
        'initial_temperature': 1000,
        'final_temperature': 1,
        'cooling_rate': 0.99,
        'max_iterations': 100
    },
    'hybrid_params': {
        'local_search_iterations': 50,
        'local_search_probability': 0.3,
        'sa_iterations_per_generation': 10
    }
}

# Helper function to create and run the optimal algorithm with default settings
def generate_timetable(input_data, algorithm_type='hybrid', custom_params=None):
    """
    Generate a timetable using the specified algorithm.
    
    Args:
        input_data: JSON data containing resources and constraints
        algorithm_type: 'ga', 'sa', 'cp', or 'hybrid'
        custom_params: Optional custom parameters for the algorithm
        
    Returns:
        A generated timetable that satisfies constraints
    """
    params = custom_params or DEFAULT_CONFIG
    
    if algorithm_type.lower() == 'ga':
        algorithm = GeneticAlgorithm(input_data, params['ga_params'])
    elif algorithm_type.lower() == 'sa':
        algorithm = SimulatedAnnealing(input_data, params['sa_params'])
    elif algorithm_type.lower() == 'cp':
        algorithm = ConstraintProgramming(input_data)
    elif algorithm_type.lower() == 'hybrid':
        algorithm = HybridAlgorithm(input_data, params)
    else:
        raise ValueError(f"Unknown algorithm type: {algorithm_type}")
    
    return algorithm.run()
