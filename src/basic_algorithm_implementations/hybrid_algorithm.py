"""
Hybrid Algorithm implementation that combines Genetic Algorithm and Simulated Annealing.
Based on Section 8 of the research paper.
"""

from typing import Dict, Any, List
import random
import math
import numpy as np
from tqdm import tqdm
from .genetic_algorithm import GeneticAlgorithm
from .simulated_annealing import SimulatedAnnealing

class HybridAlgorithm:
    def __init__(self, data: Dict[str, Any], params: Dict[str, Any] = None):
        self.data = data
        
        # Use default parameters if none provided
        self.params = params or {}
        
        # Initialize GA parameters
        self.ga_params = self.params.get('ga_params', {
            'population_size': 300,  # As per Section 8.5.1.2
            'generations': 500,      # As per Section 8.5.1.2
            'mutation_rate': 0.2,    # As per Section 8.5.1.2
            'crossover_rate': 0.8,   # As per Section 8.5.1.2
            'selection_method': 'tournament',
            'tournament_size': 3,
            'elitism_count': 5
        })
        
        # Initialize SA parameters
        self.sa_params = self.params.get('sa_params', {
            'initial_temperature': 1000,  # As per Section 8.5.1.2
            'final_temperature': 1,       # As per Section 8.5.1.2
            'cooling_rate': 0.99,         # As per Section 8.5.1.2
            'max_iterations': 100         # As per Section 8.5.1.2
        })
        
        # Initialize hybrid parameters
        self.hybrid_params = self.params.get('hybrid_params', {
            'local_search_iterations': 50,
            'local_search_probability': 0.3,
            'sa_iterations_per_generation': 10,
            'population_replacement_strategy': 'worst',
            'convergence_threshold': 0.001,
            'max_stagnation_generations': 20
        })
        
        # Initialize GA component
        self.ga = GeneticAlgorithm(data, self.ga_params)
        
        # Will initialize SA component when needed
        self.sa = None
        
        # Tracking for convergence
        self.best_fitness_history = []
        self.stagnation_count = 0
    
    def _apply_sa_to_solution(self, solution: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply Simulated Annealing to refine a solution.
        This is a key part of the hybrid approach described in Section 8.
        """
        # Create temporary SA instance with the solution as initial state
        sa = SimulatedAnnealing(self.data, self.sa_params)
        sa.current_solution = solution.copy()
        sa.best_solution = solution.copy()
        sa.current_cost = sa._calculate_cost(solution)
        sa.best_cost = sa.current_cost
        
        # Run SA for a limited number of iterations
        temperature = self.sa_params.get('initial_temperature', 1000)
        cooling_rate = self.sa_params.get('cooling_rate', 0.99)
        
        for _ in range(self.hybrid_params.get('sa_iterations_per_generation', 10)):
            # Generate a neighbor
            neighbor = sa._generate_neighbor(sa.current_solution)
            
            # Calculate the cost of the neighbor
            neighbor_cost = sa._calculate_cost(neighbor)
            
            # Decide whether to accept the neighbor
            if sa._acceptance_probability(sa.current_cost, neighbor_cost, temperature) > random.random():
                sa.current_solution = neighbor
                sa.current_cost = neighbor_cost
                
                # Update best solution if needed
                if neighbor_cost < sa.best_cost:
                    sa.best_solution = neighbor.copy()
                    sa.best_cost = neighbor_cost
            
            # Cool down
            temperature *= cooling_rate
        
        return sa.best_solution
    
    def _check_convergence(self) -> bool:
        """
        Check if the algorithm has converged.
        """
        # If we have a fitness history of at least 10 generations
        if len(self.best_fitness_history) >= 10:
            # Calculate the change in fitness over the last 10 generations
            fitness_change = abs(self.best_fitness_history[-1] - self.best_fitness_history[-10]) / abs(self.best_fitness_history[-10]) if self.best_fitness_history[-10] != 0 else 0
            
            # If the change is below the threshold
            if fitness_change < self.hybrid_params.get('convergence_threshold', 0.001):
                self.stagnation_count += 1
            else:
                self.stagnation_count = 0
            
            # If we've been stagnant for too long, consider the algorithm converged
            return self.stagnation_count >= self.hybrid_params.get('max_stagnation_generations', 20)
        
        return False
    
    def run(self) -> Dict[str, Any]:
        """
        Run the hybrid algorithm.
        Following Section 8 of the paper.
        """
        # Initialize GA population
        self.ga.population = self.ga._initialize_population()
        
        # Create progress bar
        pbar = tqdm(total=self.ga_params['generations'], desc="Running Hybrid Algorithm")
        
        for generation in range(self.ga_params['generations']):
            # Evaluate population
            fitness_values = [self.ga._calculate_fitness(t) for t in self.ga.population]
            
            # Update best solution
            max_fitness_idx = fitness_values.index(max(fitness_values))
            if fitness_values[max_fitness_idx] > self.ga.best_fitness:
                self.ga.best_fitness = fitness_values[max_fitness_idx]
                self.ga.best_solution = self.ga.population[max_fitness_idx].copy()
            
            # Record best fitness for convergence check
            self.best_fitness_history.append(self.ga.best_fitness)
            
            # Create new population
            new_population = []
            
            # Elitism: keep the best solutions
            elitism_count = self.ga_params['elitism_count']
            sorted_indices = np.argsort(fitness_values)[::-1]  # Descending order
            for i in range(min(elitism_count, len(self.ga.population))):
                elite_solution = self.ga.population[sorted_indices[i]].copy()
                
                # Apply SA to some elite solutions
                if random.random() < self.hybrid_params.get('local_search_probability', 0.3):
                    elite_solution = self._apply_sa_to_solution(elite_solution)
                
                new_population.append(elite_solution)
            
            # Generate new solutions through selection, crossover, and mutation
            while len(new_population) < self.ga_params['population_size']:
                parent1, parent2 = self.ga._selection()
                child = self.ga._crossover(parent1, parent2)
                child = self.ga._mutation(child)
                
                # Apply SA to some children
                if random.random() < self.hybrid_params.get('local_search_probability', 0.3):
                    child = self._apply_sa_to_solution(child)
                
                new_population.append(child)
            
            self.ga.population = new_population
            
            # Update progress bar
            pbar.update(1)
            
            # Print progress periodically
            if generation % 100 == 0 or generation == self.ga_params['generations'] - 1:
                pbar.set_description(f"Generation {generation}: Best Fitness = {self.ga.best_fitness}")
            
            # Check for convergence
            if self._check_convergence():
                print(f"Algorithm converged after {generation} generations")
                break
        
        pbar.close()
        
        # Apply final SA refinement to the best solution
        print("Applying final refinement with Simulated Annealing...")
        final_solution = self._apply_sa_to_solution(self.ga.best_solution)
        
        return final_solution
