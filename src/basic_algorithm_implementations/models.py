# src/models.py
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional, Any

@dataclass
class Teacher:
    id: str
    name: str
    department: str
    specialization: List[str]
    max_hours_per_day: int
    max_hours_per_week: int
    preferences: Dict[str, List[str]]
    unavailability: List[Dict[str, Any]]
    is_mentor: bool
    max_mentees: int = 4

@dataclass
class Student:
    id: str
    name: str
    batch: str
    semester: int
    registered_courses: List[str]
    needs_mentor: bool
    special_requirements: List[str] = field(default_factory=list)

@dataclass
class Course:
    id: str
    code: str
    name: str
    credits: int
    hours_per_week: int
    sessions_per_week: int
    session_duration: int
    requires_lab: bool
    preferred_rooms: List[str]
    eligible_teachers: List[str]
    student_groups: List[str]

@dataclass
class Room:
    id: str
    name: str
    type: str
    capacity: int
    facilities: List[str]
    building: str
    floor: int

@dataclass
class TimeSlot:
    id: str
    day: str
    start_time: str
    end_time: str
    type: str

@dataclass
class StudentGroup:
    id: str
    name: str
    students: List[str]
    courses: List[str]

@dataclass
class Constraint:
    type: str
    description: str
    weight: int
