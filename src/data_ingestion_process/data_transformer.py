"""
Data Transformer module for Timetable Generation System.
Transforms input JSON data into the format required by the algorithms.
"""

import logging
from typing import Dict, Any, List
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataTransformer:
    """
    Class for transforming input data into the format expected by timetable algorithms.
    """
    
    def __init__(self):
        """Initialize the DataTransformer."""
        pass
    
    def transform(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform raw input data into the format expected by timetable generation algorithms.
        
        Args:
            data (Dict[str, Any]): Raw input data from JSON
            
        Returns:
            Dict[str, Any]: Transformed data ready for algorithm processing
        """
        logger.info("Transforming input data for algorithm processing")
        
        transformed_data = {
            'teachers': {},
            'students': {},
            'courses': {},
            'rooms': {},
            'time_slots': {},
            'student_groups': {},
            'hard_constraints': [],
            'soft_constraints': []
        }
        
        # Transform resources
        self._transform_teachers(data, transformed_data)
        self._transform_students(data, transformed_data)
        self._transform_courses(data, transformed_data)
        self._transform_rooms(data, transformed_data)
        self._transform_time_slots(data, transformed_data)
        self._transform_student_groups(data, transformed_data)
        
        # Transform constraints
        self._transform_constraints(data, transformed_data)
        
        # Add algorithm parameters if provided
        if "algorithm_parameters" in data:
            transformed_data["algorithm_parameters"] = data["algorithm_parameters"]
        
        # Add metadata
        transformed_data["metadata"] = data.get("metadata", {})
        transformed_data["metadata"]["transformed_at"] = datetime.now().isoformat()
        
        logger.info("Data transformation completed successfully")
        return transformed_data
    
    def _transform_teachers(self, data: Dict[str, Any], transformed_data: Dict[str, Any]) -> None:
        """Transform teacher data into dictionary keyed by ID."""
        resources = data.get("resources", {})
        teachers = resources.get("teachers", [])
        
        for teacher in teachers:
            teacher_id = teacher["id"]
            transformed_data["teachers"][teacher_id] = self._create_teacher_object(teacher)
    
    def _create_teacher_object(self, teacher_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a structured teacher object with all required fields."""
        return {
            "id": teacher_data["id"],
            "name": teacher_data["name"],
            "department": teacher_data.get("department", ""),
            "specialization": teacher_data.get("specialization", []),
            "max_hours_per_day": teacher_data.get("max_hours_per_day", 8),
            "max_hours_per_week": teacher_data.get("max_hours_per_week", 40),
            "preferences": teacher_data.get("preferences", {}),
            "unavailability": teacher_data.get("unavailability", []),
            "is_mentor": teacher_data.get("is_mentor", False),
            "max_mentees": teacher_data.get("max_mentees", 4)
        }
    
    def _transform_students(self, data: Dict[str, Any], transformed_data: Dict[str, Any]) -> None:
        """Transform student data into dictionary keyed by ID."""
        resources = data.get("resources", {})
        students = resources.get("students", [])
        
        for student in students:
            student_id = student["id"]
            transformed_data["students"][student_id] = self._create_student_object(student)
    
    def _create_student_object(self, student_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a structured student object with all required fields."""
        return {
            "id": student_data["id"],
            "name": student_data["name"],
            "batch": student_data.get("batch", ""),
            "semester": student_data.get("semester", 1),
            "registered_courses": student_data.get("registered_courses", []),
            "needs_mentor": student_data.get("needs_mentor", False),
            "special_requirements": student_data.get("special_requirements", [])
        }
    
    def _transform_courses(self, data: Dict[str, Any], transformed_data: Dict[str, Any]) -> None:
        """Transform course data into dictionary keyed by ID."""
        resources = data.get("resources", {})
        courses = resources.get("courses", [])
        
        for course in courses:
            course_id = course["id"]
            transformed_data["courses"][course_id] = self._create_course_object(course)
    
    def _create_course_object(self, course_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a structured course object with all required fields."""
        return {
            "id": course_data["id"],
            "code": course_data["code"],
            "name": course_data["name"],
            "credits": course_data.get("credits", 0),
            "hours_per_week": course_data.get("hours_per_week", 0),
            "sessions_per_week": course_data.get("sessions_per_week", 1),
            "session_duration": course_data.get("session_duration", 1),
            "requires_lab": course_data.get("requires_lab", False),
            "preferred_rooms": course_data.get("preferred_rooms", []),
            "eligible_teachers": course_data.get("eligible_teachers", []),
            "student_groups": course_data.get("student_groups", [])
        }
    
    def _transform_rooms(self, data: Dict[str, Any], transformed_data: Dict[str, Any]) -> None:
        """Transform room data into dictionary keyed by ID."""
        resources = data.get("resources", {})
        rooms = resources.get("rooms", [])
        
        for room in rooms:
            room_id = room["id"]
            transformed_data["rooms"][room_id] = self._create_room_object(room)
    
    def _create_room_object(self, room_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a structured room object with all required fields."""
        return {
            "id": room_data["id"],
            "name": room_data["name"],
            "type": room_data.get("type", "Lecture Hall"),
            "capacity": room_data.get("capacity", 0),
            "facilities": room_data.get("facilities", []),
            "building": room_data.get("building", ""),
            "floor": room_data.get("floor", 0)
        }
    
    def _transform_time_slots(self, data: Dict[str, Any], transformed_data: Dict[str, Any]) -> None:
        """Transform time slot data into dictionary keyed by ID."""
        resources = data.get("resources", {})
        time_slots = resources.get("time_slots", [])
        
        for time_slot in time_slots:
            time_slot_id = time_slot["id"]
            transformed_data["time_slots"][time_slot_id] = self._create_time_slot_object(time_slot)
    
    def _create_time_slot_object(self, time_slot_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a structured time slot object with all required fields."""
        return {
            "id": time_slot_data["id"],
            "day": time_slot_data["day"],
            "start_time": time_slot_data["start_time"],
            "end_time": time_slot_data["end_time"],
            "type": time_slot_data.get("type", "Regular")
        }
    
    def _transform_student_groups(self, data: Dict[str, Any], transformed_data: Dict[str, Any]) -> None:
        """Transform student group data into dictionary keyed by ID."""
        resources = data.get("resources", {})
        student_groups = resources.get("student_groups", [])
        
        for group in student_groups:
            group_id = group["id"]
            transformed_data["student_groups"][group_id] = self._create_student_group_object(group)
    
    def _create_student_group_object(self, group_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a structured student group object with all required fields."""
        return {
            "id": group_data["id"],
            "name": group_data["name"],
            "students": group_data.get("students", []),
            "courses": group_data.get("courses", [])
        }
    
    def _transform_constraints(self, data: Dict[str, Any], transformed_data: Dict[str, Any]) -> None:
        """Transform constraints into the format expected by algorithms."""
        constraints = data.get("constraints", {})
        
        # Transform hard constraints
        hard_constraints = constraints.get("hard_constraints", [])
        for constraint in hard_constraints:
            transformed_data["hard_constraints"].append({
                "type": constraint["type"],
                "description": constraint["description"],
                "weight": constraint["weight"]
            })
        
        # Transform soft constraints
        soft_constraints = constraints.get("soft_constraints", [])
        for constraint in soft_constraints:
            transformed_data["soft_constraints"].append({
                "type": constraint["type"],
                "description": constraint["description"],
                "weight": constraint["weight"]
            })
