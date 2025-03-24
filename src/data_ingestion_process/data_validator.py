"""
Data Validator module for Timetable Generation System.
Validates input JSON data against expected schema and constraints.
"""

import json
import logging
from typing import Dict, Any, List, Optional, Tuple

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataValidator:
    """
    Class for validating input data for timetable generation.
    Ensures data structure and content meet required specifications.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the DataValidator.
        
        Args:
            config_path (str, optional): Path to configuration file for custom validation rules
        """
        # Default validation configuration
        self.config = {
            "required_sections": ["metadata", "resources", "constraints"],
            "required_resources": ["teachers", "students", "courses", "rooms", "time_slots", "student_groups"],
            "required_constraints": ["hard_constraints", "soft_constraints"],
            "required_fields": {
                "teachers": ["id", "name", "department", "is_mentor"],
                "students": ["id", "name", "batch", "registered_courses", "needs_mentor"],
                "courses": ["id", "code", "name", "credits", "eligible_teachers", "student_groups"],
                "rooms": ["id", "name", "type", "capacity"],
                "time_slots": ["id", "day", "start_time", "end_time"],
                "student_groups": ["id", "name", "students", "courses"]
            }
        }
        
        # Load custom configuration if provided
        if config_path:
            try:
                with open(config_path, 'r') as f:
                    custom_config = json.load(f)
                    self.config.update(custom_config)
                logger.info(f"Loaded custom validation configuration from {config_path}")
            except Exception as e:
                logger.warning(f"Failed to load custom configuration from {config_path}: {str(e)}")
    
    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the input data against expected structure and constraints.
        
        Args:
            data (Dict[str, Any]): Input data to validate
            
        Returns:
            Dict[str, Any]: Validation result with is_valid flag and any errors
        """
        logger.info("Validating input data")
        
        errors = []
        
        # Check required sections
        section_errors = self._validate_required_sections(data)
        errors.extend(section_errors)
        
        # If missing required sections, don't continue validation
        if section_errors:
            return {
                "is_valid": False,
                "errors": errors
            }
        
        # Check resources section
        resource_errors = self._validate_resources(data["resources"])
        errors.extend(resource_errors)
        
        # Check constraints section
        constraint_errors = self._validate_constraints(data["constraints"])
        errors.extend(constraint_errors)
        
        # Validate relationships and cross-references
        relation_errors = self._validate_relationships(data)
        errors.extend(relation_errors)
        
        # Check for mentor group size constraint (exactly 4 students per mentor)
        mentor_errors = self._validate_mentor_assignments(data)
        errors.extend(mentor_errors)
        
        validation_result = {
            "is_valid": len(errors) == 0,
            "errors": errors
        }
        
        if validation_result["is_valid"]:
            logger.info("Input data validation successful")
        else:
            logger.error(f"Input data validation failed with {len(errors)} errors")
        
        return validation_result
    
    def _validate_required_sections(self, data: Dict[str, Any]) -> List[str]:
        """Validate that all required sections are present in the data."""
        errors = []
        
        for section in self.config["required_sections"]:
            if section not in data:
                errors.append(f"Missing required section: {section}")
        
        return errors
    
    def _validate_resources(self, resources: Dict[str, Any]) -> List[str]:
        """Validate the resources section of the data."""
        errors = []
        
        # Check that all required resource types are present
        for resource_type in self.config["required_resources"]:
            if resource_type not in resources:
                errors.append(f"Missing required resource type: {resource_type}")
                continue
            
            # Check that each resource has required fields
            required_fields = self.config["required_fields"].get(resource_type, [])
            for i, resource in enumerate(resources[resource_type]):
                for field in required_fields:
                    if field not in resource:
                        errors.append(f"{resource_type}[{i}] is missing required field: {field}")
        
        return errors
    
    def _validate_constraints(self, constraints: Dict[str, Any]) -> List[str]:
        """Validate the constraints section of the data."""
        errors = []
        
        # Check that all required constraint types are present
        for constraint_type in self.config["required_constraints"]:
            if constraint_type not in constraints:
                errors.append(f"Missing required constraint type: {constraint_type}")
                continue
            
            # Check that each constraint has type, description, and weight
            for i, constraint in enumerate(constraints[constraint_type]):
                if "type" not in constraint:
                    errors.append(f"{constraint_type}[{i}] is missing required field: type")
                if "description" not in constraint:
                    errors.append(f"{constraint_type}[{i}] is missing required field: description")
                if "weight" not in constraint:
                    errors.append(f"{constraint_type}[{i}] is missing required field: weight")
        
        return errors
    
    def _validate_relationships(self, data: Dict[str, Any]) -> List[str]:
        """Validate relationships and cross-references between different resources."""
        errors = []
        resources = data["resources"]
        
        # Check that all eligible_teachers for courses exist in teachers list
        teacher_ids = set(t["id"] for t in resources["teachers"])
        for i, course in enumerate(resources["courses"]):
            for teacher_id in course.get("eligible_teachers", []):
                if teacher_id not in teacher_ids:
                    errors.append(f"Course {course['id']} references non-existent teacher: {teacher_id}")
        
        # Check that all student_groups for courses exist in student_groups list
        group_ids = set(g["id"] for g in resources["student_groups"])
        for i, course in enumerate(resources["courses"]):
            for group_id in course.get("student_groups", []):
                if group_id not in group_ids:
                    errors.append(f"Course {course['id']} references non-existent student group: {group_id}")
        
        # Check that all students in student_groups exist in students list
        student_ids = set(s["id"] for s in resources["students"])
        for i, group in enumerate(resources["student_groups"]):
            for student_id in group.get("students", []):
                if student_id not in student_ids:
                    errors.append(f"Student group {group['id']} references non-existent student: {student_id}")
        
        # Check that all preferred_rooms for courses exist in rooms list
        room_ids = set(r["id"] for r in resources["rooms"])
        for i, course in enumerate(resources["courses"]):
            for room_id in course.get("preferred_rooms", []):
                if room_id not in room_ids:
                    errors.append(f"Course {course['id']} references non-existent room: {room_id}")
        
        return errors
    
    def _validate_mentor_assignments(self, data: Dict[str, Any]) -> List[str]:
        """
        Validate that mentor assignments follow the 4 students per mentor rule
        as specified in the problem statement.
        """
        errors = []
        resources = data["resources"]
        
        # Find mentors
        mentors = [t for t in resources["teachers"] if t.get("is_mentor", False)]
        
        # Check if the student groups assigned to mentors have exactly 4 students
        for group in resources["student_groups"]:
            if len(group.get("students", [])) != 4:
                errors.append(f"Student group {group['id']} does not have exactly 4 students as required for mentor assignment")
        
        return errors
