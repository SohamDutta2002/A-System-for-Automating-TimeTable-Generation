"""
Constraint Programming implementation for timetable generation.
Based on Section 6 of the research paper.
"""

from typing import Dict, Any, List, Tuple
from tqdm import tqdm
import random

class ConstraintProgramming:
    def __init__(self, data: Dict[str, Any], params: Dict[str, Any] = None):
        self.data = data
        self.params = params or {
            'max_iterations': 1000,
            'max_unassigned': 0
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
        self.current_solution = {}
    
    def _check_constraints(self, solution: Dict[str, Any], course_id: str,
                           teacher_id: str, room_id: str, time_slot_id: str) -> bool:
        """
        Check if assigning a course to a teacher, room, and time slot violates any hard constraints.
        """
        # Check teacher availability for this time slot
        for existing_course_id, assignment in solution.items():
            if assignment['teacher_id'] == teacher_id and assignment['time_slot_id'] == time_slot_id:
                return False  # Teacher already assigned at this time slot
        
        # Check room availability for this time slot
        for existing_course_id, assignment in solution.items():
            if assignment['room_id'] == room_id and assignment['time_slot_id'] == time_slot_id:
                return False  # Room already assigned at this time slot
        
        # Check student group availability for this time slot
        course = self.courses.get(course_id)
        if course:
            for group_id in course.student_groups:
                for existing_course_id, assignment in solution.items():
                    existing_course = self.courses.get(existing_course_id)
                    if existing_course and group_id in existing_course.student_groups and assignment['time_slot_id'] == time_slot_id:
                        return False  # Student group already has a class at this time slot
        
        return True  # No constraints violated
    
    def _backtracking_search(self) -> Dict[str, Any]:
        """
        Use backtracking search to find a valid assignment.
        This is a simplified version of the full CP approach described in Section 6.
        """
        solution = {}
        unassigned_courses = list(self.courses.keys())
        
        # Sort courses by the number of constraints (courses with more constraints first)
        unassigned_courses.sort(key=lambda c: len(self.courses[c].eligible_teachers) * 
                                            len(self.courses[c].preferred_rooms))
        
        return self._backtrack(solution, unassigned_courses)
    
    def _backtrack(self, solution: Dict[str, Any], unassigned_courses: List[str]) -> Dict[str, Any]:
        """
        Recursive backtracking algorithm for constraint satisfaction.
        """
        if not unassigned_courses:
            return solution  # All courses assigned
        
        # Select the next course to assign
        course_id = unassigned_courses[0]
        course = self.courses[course_id]
        
        # Try all possible teacher, room, time slot combinations
        for teacher_id in course.eligible_teachers:
            for room_id in course.preferred_rooms:
                for time_slot_id in self.time_slots:
                    # Check if this assignment satisfies all constraints
                    if self._check_constraints(solution, course_id, teacher_id, room_id, time_slot_id):
                        # Assign the course
                        solution[course_id] = {
                            'teacher_id': teacher_id,
                            'room_id': room_id,
                            'time_slot_id': time_slot_id
                        }
                        
                        # Recursively assign the next course
                        result = self._backtrack(solution, unassigned_courses[1:])
                        if result:
                            return result
                        
                        # If we get here, the assignment didn't work, so undo it
                        del solution[course_id]
        
        return None  # No valid assignment found
    
    def _iterative_forward_checking(self) -> Dict[str, Any]:
        """
        Implement iterative forward checking to find a valid assignment.
        More efficient than pure backtracking for large problems.
        """
        max_iterations = self.params['max_iterations']
        max_unassigned = self.params['max_unassigned']
        
        best_solution = {}
        best_unassigned = len(self.courses)
        
        # Create progress bar
        pbar = tqdm(total=max_iterations, desc="Running Constraint Programming")
        
        for iteration in range(max_iterations):
            solution = {}
            unassigned = []
            
            # Try to assign each course
            for course_id, course in self.courses.items():
                # Create a list of all possible assignments
                assignments = []
                for teacher_id in course.eligible_teachers:
                    for room_id in course.preferred_rooms:
                        for time_slot_id in self.time_slots:
                            if self._check_constraints(solution, course_id, teacher_id, room_id, time_slot_id):
                                assignments.append((teacher_id, room_id, time_slot_id))
                
                if assignments:
                    # Pick a random valid assignment
                    teacher_id, room_id, time_slot_id = random.choice(assignments)
                    solution[course_id] = {
                        'teacher_id': teacher_id,
                        'room_id': room_id,
                        'time_slot_id': time_slot_id
                    }
                else:
                    unassigned.append(course_id)
            
            # Update best solution if this one is better
            if len(unassigned) < best_unassigned:
                best_solution = solution.copy()
                best_unassigned = len(unassigned)
                
                pbar.set_description(f"Iteration {iteration}: Unassigned = {best_unassigned}")
                
                if best_unassigned <= max_unassigned:
                    break  # Found a good enough solution
            
            pbar.update(1)
        
        pbar.close()
        return best_solution
    
    def run(self) -> Dict[str, Any]:
        """
        Run the constraint programming algorithm.
        """
        # Try backtracking search for small problems
        if len(self.courses) <= 20:
            print("Using backtracking search for small problem...")
            solution = self._backtracking_search()
            if solution:
                return solution
        
        # Use iterative forward checking for larger problems
        print("Using iterative forward checking...")
        return self._iterative_forward_checking()
