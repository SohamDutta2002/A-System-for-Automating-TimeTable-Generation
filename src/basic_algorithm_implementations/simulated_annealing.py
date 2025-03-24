"""
Simulated Annealing implementation for timetable generation.
Based on Section 5 of the research paper.
"""

import random
import math
from typing import Dict, Any, List, Tuple
from tqdm import tqdm

class SimulatedAnnealing:
    def __init__(self, data: Dict[str, Any], params: Dict[str, Any] = None):
        self.data = data
        self.params = params or {
            'initial_temperature': 1000,  # As per Section 8.5.1.2
            'final_temperature': 1,       # As per Section 8.5.1.2
            'cooling_rate': 0.99,         # As per Section 8.5.1.2
            'max_iterations': 100         # As per Section 8.5.1.2
        }
        
        # Extract resources
        self.teachers = data['teachers']
        self.courses = data['courses']
        self.rooms = data['rooms']
        self.time_slots = data['time_slots']
        self.student_groups = data['student_groups']
        self.hard_constraints = data['hard_constraints']
        self.soft_constraints = data['soft_constraints']
        
        # Initialize solution
        self.current_solution = self._generate_initial_solution()
        self.best_solution = self.current_solution.copy()
        self.current_cost = self._calculate_cost(self.current_solution)
        self.best_cost = self.current_cost
    
    def _generate_initial_solution(self) -> Dict[str, Any]:
        """
        Generate an initial random solution.
        Following Section 5.2 of the paper.
        """
        solution = {}
        
        # For each course, randomly assign a teacher, room, and time slot
        for course_id, course in self.courses.items():
            eligible_teachers = course.eligible_teachers
            if not eligible_teachers:
                continue  # Skip if no eligible teachers
                
            teacher_id = random.choice(eligible_teachers)
            
            # Choose a random room from preferred rooms
            if not course.preferred_rooms:
                continue  # Skip if no preferred rooms
                
            room_id = random.choice(course.preferred_rooms)
            
            # Choose a random time slot
            if not self.time_slots:
                continue  # Skip if no time slots available
                
            time_slot_id = random.choice(list(self.time_slots.keys()))
            
            solution[course_id] = {
                'teacher_id': teacher_id,
                'room_id': room_id,
                'time_slot_id': time_slot_id
            }
        
        return solution
    
    def _calculate_cost(self, solution: Dict[str, Any]) -> float:
        """
        Calculate the cost (penalty) of a solution.
        Following Section 5.3 of the paper.
        """
        # Initialize penalties for constraint violations
        violations = {
            "teacher_overlap": 0,
            "room_overlap": 0,
            "mentor_group_size": 0,
            "back_to_back_sessions": 0,
            "equitable_teaching_load": 0
        }
        
        # Check for teacher overlaps (hard constraint)
        teacher_timeslots = {}
        for course_id, assignment in solution.items():
            teacher_id = assignment['teacher_id']
            time_slot_id = assignment['time_slot_id']
            
            if teacher_id not in teacher_timeslots:
                teacher_timeslots[teacher_id] = set()
            
            if time_slot_id in teacher_timeslots[teacher_id]:
                violations["teacher_overlap"] += 1
            else:
                teacher_timeslots[teacher_id].add(time_slot_id)
        
        # Check for room overlaps (hard constraint)
        room_timeslots = {}
        for course_id, assignment in solution.items():
            room_id = assignment['room_id']
            time_slot_id = assignment['time_slot_id']
            
            if room_id not in room_timeslots:
                room_timeslots[room_id] = set()
            
            if time_slot_id in room_timeslots[room_id]:
                violations["room_overlap"] += 1
            else:
                room_timeslots[room_id].add(time_slot_id)
        
        # Check mentor group size (hard constraint in the paper)
        mentor_students = {}
        for teacher_id, teacher in self.teachers.items():
            if teacher.is_mentor:
                mentor_students[teacher_id] = set()
        
        # Collect students for each mentor based on course assignments
        for course_id, assignment in solution.items():
            teacher_id = assignment['teacher_id']
            if teacher_id in mentor_students:
                course = self.courses.get(course_id)
                if course:
                    for group_id in course.student_groups:
                        group = self.student_groups.get(group_id)
                        if group:
                            mentor_students[teacher_id].update(group.students)
        
        # Penalize incorrect mentor group sizes
        for teacher_id, students in mentor_students.items():
            if len(students) != 4:  # The paper specifies exactly 4 students per mentor
                violations["mentor_group_size"] += abs(len(students) - 4)
        
        # Compute penalties for hard constraints
        hard_penalty = (
            100 * violations["teacher_overlap"] + 
            100 * violations["room_overlap"] + 
            100 * violations["mentor_group_size"]
        )
        
        # Compute penalties for soft constraints
        soft_penalty = (
            50 * violations["back_to_back_sessions"] + 
            40 * violations["equitable_teaching_load"]
        )
        
        # Calculate total cost (sum of penalties)
        # Unlike fitness, cost is positive and should be minimized
        cost = hard_penalty + soft_penalty
        
        return cost
    
    def _generate_neighbor(self, solution: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a neighboring solution by making a small change.
        Following Section 5.4 of the paper.
        """
        neighbor = solution.copy()
        
        if not self.courses:
            return neighbor  # No courses to modify
        
        # Randomly select a course to modify
        course_id = random.choice(list(neighbor.keys()))
        course = self.courses.get(course_id)
        
        if not course:
            return neighbor  # Course not found
        
        # Choose what to modify: teacher, room, or time slot
        modification = random.choice(['teacher', 'room', 'time_slot'])
        
        if modification == 'teacher' and course.eligible_teachers:
            neighbor[course_id]['teacher_id'] = random.choice(course.eligible_teachers)
        elif modification == 'room' and course.preferred_rooms:
            neighbor[course_id]['room_id'] = random.choice(course.preferred_rooms)
        elif modification == 'time_slot' and self.time_slots:
            neighbor[course_id]['time_slot_id'] = random.choice(list(self.time_slots.keys()))
        
        return neighbor
    
    def _acceptance_probability(self, current_cost: float, new_cost: float, temperature: float) -> float:
        """
        Calculate the probability of accepting a worse solution.
        Following Section 5.5 of the paper.
        """
        if new_cost < current_cost:
            return 1.0  # Always accept better solutions
        
        # For worse solutions, acceptance probability decreases as temperature decreases
        # and as the cost difference increases
        return math.exp((current_cost - new_cost) / temperature)
    
    def run(self) -> Dict[str, Any]:
        """
        Run the simulated annealing algorithm.
        Following Section 5.8 of the paper.
        """
        temperature = self.params['initial_temperature']
        
        # Create progress bar
        total_iterations = 0
        while temperature > self.params['final_temperature'] and total_iterations < self.params['max_iterations']:
            total_iterations += 1
        
        pbar = tqdm(total=total_iterations, desc="Running Simulated Annealing")
        
        iteration = 0
        while temperature > self.params['final_temperature'] and iteration < self.params['max_iterations']:
            # Generate a neighbor
            neighbor = self._generate_neighbor(self.current_solution)
            
            # Calculate the cost of the neighbor
            neighbor_cost = self._calculate_cost(neighbor)
            
            # Decide whether to accept the neighbor
            if self._acceptance_probability(self.current_cost, neighbor_cost, temperature) > random.random():
                self.current_solution = neighbor
                self.current_cost = neighbor_cost
                
                # Update best solution if needed
                if neighbor_cost < self.best_cost:
                    self.best_solution = neighbor.copy()
                    self.best_cost = neighbor_cost
            
            # Cool down
            temperature *= self.params['cooling_rate']
            iteration += 1
            
            # Update progress bar
            pbar.update(1)
            
            # Print progress periodically
            if iteration % 10 == 0 or iteration == self.params['max_iterations'] - 1:
                pbar.set_description(f"Iteration {iteration}: Temperature = {temperature:.2f}, Best Cost = {self.best_cost}")
        
        pbar.close()
        return self.best_solution
