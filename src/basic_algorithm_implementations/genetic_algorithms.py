# src/genetic_algorithm.py
import random
from typing import Dict, Any, List, Tuple
import numpy as np

class GeneticAlgorithm:
    def __init__(self, data: Dict[str, Any], params: Dict[str, Any] = None):
        self.data = data
        self.params = params or {
            'population_size': 300,
            'generations': 500,
            'mutation_rate': 0.2,
            'crossover_rate': 0.8,
            'selection_method': 'tournament',
            'tournament_size': 3,
            'elitism_count': 5
        }
        
        # Extract resources
        self.teachers = data['teachers']
        self.courses = data['courses']
        self.rooms = data['rooms']
        self.time_slots = data['time_slots']
        self.student_groups = data['student_groups']
        
        # Initialize population
        self.population = self._initialize_population()
        self.best_solution = None
        self.best_fitness = float('-inf')
    
    def _initialize_population(self) -> List[Dict[str, Any]]:
        """Initialize a random population of timetables."""
        population = []
        for _ in range(self.params['population_size']):
            timetable = self._generate_random_timetable()
            population.append(timetable)
        return population
    
    def _generate_random_timetable(self) -> Dict[str, Any]:
        """Generate a random timetable."""
        timetable = {}
        
        # For each course, randomly assign a teacher, room, and time slot
        for course_id, course in self.courses.items():
            eligible_teachers = course.eligible_teachers
            teacher_id = random.choice(eligible_teachers)
            
            # Choose a random room and time slot
            room_id = random.choice(course.preferred_rooms)
            # Simplistic assignment - in a real implementation, check for conflicts
            time_slot_id = random.choice(list(self.time_slots.keys()))
            
            timetable[course_id] = {
                'teacher_id': teacher_id,
                'room_id': room_id,
                'time_slot_id': time_slot_id
            }
        
        return timetable
    
    def _calculate_fitness(self, timetable: Dict[str, Any]) -> float:
        """Calculate fitness of a timetable based on constraints."""
        # Initialize penalties
        teacher_conflict_penalty = 0
        room_conflict_penalty = 0
        mentor_group_penalty = 0
        
        # Check for teacher conflicts
        teacher_timeslots = {}
        for course_id, assignment in timetable.items():
            teacher_id = assignment['teacher_id']
            time_slot_id = assignment['time_slot_id']
            
            if teacher_id not in teacher_timeslots:
                teacher_timeslots[teacher_id] = set()
            
            if time_slot_id in teacher_timeslots[teacher_id]:
                teacher_conflict_penalty += 100  # High penalty for hard constraint
            else:
                teacher_timeslots[teacher_id].add(time_slot_id)
        
        # Check for room conflicts
        room_timeslots = {}
        for course_id, assignment in timetable.items():
            room_id = assignment['room_id']
            time_slot_id = assignment['time_slot_id']
            
            if room_id not in room_timeslots:
                room_timeslots[room_id] = set()
            
            if time_slot_id in room_timeslots[room_id]:
                room_conflict_penalty += 100  # High penalty for hard constraint
            else:
                room_timeslots[room_id].add(time_slot_id)
        
        # Check mentor group size (simplified)
        # Each mentor should have exactly 4 students
        mentor_students = {}
        for teacher_id, teacher in self.teachers.items():
            if teacher.is_mentor:
                mentor_students[teacher_id] = 0
        
        # Count students per mentor
        for group_id, group in self.student_groups.items():
            for course_id, assignment in timetable.items():
                if course_id in group.courses:
                    teacher_id = assignment['teacher_id']
                    if teacher_id in mentor_students:
                        mentor_students[teacher_id] += len(group.students)
        
        # Penalize incorrect mentor group sizes
        for teacher_id, count in mentor_students.items():
            if count != 4:
                mentor_group_penalty += 50 * abs(count - 4)
        
        # Calculate total fitness (negative sum of penalties)
        fitness = -(teacher_conflict_penalty + room_conflict_penalty + mentor_group_penalty)
        
        return fitness
    
    def _selection(self) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Select two parents using tournament selection."""
        tournament_size = self.params['tournament_size']
        
        # First parent
        tournament1 = random.sample(self.population, tournament_size)
        fitness_values1 = [self._calculate_fitness(t) for t in tournament1]
        parent1 = tournament1[fitness_values1.index(max(fitness_values1))]
        
        # Second parent
        tournament2 = random.sample(self.population, tournament_size)
        fitness_values2 = [self._calculate_fitness(t) for t in tournament2]
        parent2 = tournament2[fitness_values2.index(max(fitness_values2))]
        
        return parent1, parent2
    
    def _crossover(self, parent1: Dict[str, Any], parent2: Dict[str, Any]) -> Dict[str, Any]:
        """Perform crossover between two parents."""
        if random.random() > self.params['crossover_rate']:
            return parent1.copy()
        
        child = {}
        courses = list(self.courses.keys())
        crossover_point = random.randint(1, len(courses) - 1)
        
        for i, course_id in enumerate(courses):
            if i < crossover_point:
                child[course_id] = parent1[course_id].copy()
            else:
                child[course_id] = parent2[course_id].copy()
        
        return child
    
    def _mutation(self, timetable: Dict[str, Any]) -> Dict[str, Any]:
        """Mutate a timetable."""
        for course_id in timetable:
            if random.random() < self.params['mutation_rate']:
                course = self.courses[course_id]
                
                # Randomly mutate one aspect (teacher, room, or time slot)
                mutation_type = random.choice(['teacher', 'room', 'time_slot'])
                
                if mutation_type == 'teacher' and course.eligible_teachers:
                    timetable[course_id]['teacher_id'] = random.choice(course.eligible_teachers)
                elif mutation_type == 'room' and course.preferred_rooms:
                    timetable[course_id]['room_id'] = random.choice(course.preferred_rooms)
                elif mutation_type == 'time_slot':
                    timetable[course_id]['time_slot_id'] = random.choice(list(self.time_slots.keys()))
        
        return timetable
    
    def run(self) -> Dict[str, Any]:
        """Run the genetic algorithm."""
        for generation in range(self.params['generations']):
            # Evaluate population
            fitness_values = [self._calculate_fitness(t) for t in self.population]
            
            # Update best solution
            max_fitness_idx = fitness_values.index(max(fitness_values))
            if fitness_values[max_fitness_idx] > self.best_fitness:
                self.best_fitness = fitness_values[max_fitness_idx]
                self.best_solution = self.population[max_fitness_idx].copy()
            
            # Create new population
            new_population = []
            
            # Elitism: keep the best solutions
            elitism_count = self.params['elitism_count']
            sorted_indices = np.argsort(fitness_values)[::-1]  # Descending order
            for i in range(elitism_count):
                new_population.append(self.population[sorted_indices[i]].copy())
            
            # Generate new solutions through selection, crossover, and mutation
            while len(new_population) < self.params['population_size']:
                parent1, parent2 = self._selection()
                child = self._crossover(parent1, parent2)
                child = self._mutation(child)
                new_population.append(child)
            
            self.population = new_population
            
            # Print progress
            if generation % 100 == 0:
                print(f"Generation {generation}: Best Fitness = {self.best_fitness}")
        
        return self.best_solution
