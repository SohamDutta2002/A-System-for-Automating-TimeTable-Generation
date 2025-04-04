"""
Utility functions for the timetable generation system.
"""

import json
import random
import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, Any, List, Tuple
import matplotlib.colors as mcolors
from .models import Teacher, Student, Course, Room, TimeSlot, StudentGroup, Constraint

def load_json_data(file_path: str) -> Dict[str, Any]:
    """
    Load JSON data from file and parse into appropriate data structures.
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    return parse_data(data)

def parse_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse JSON data into data model objects.
    """
    resources = data.get('resources', {})
    
    # Parse teachers
    teachers = {}
    for t in resources.get('teachers', []):
        teachers[t['id']] = Teacher(
            id=t['id'],
            name=t['name'],
            department=t['department'],
            specialization=t['specialization'],
            max_hours_per_day=t['max_hours_per_day'],
            max_hours_per_week=t['max_hours_per_week'],
            preferences=t['preferences'],
            unavailability=t['unavailability'],
            is_mentor=t['is_mentor'],
            max_mentees=t.get('max_mentees', 4)
        )
    
    # Parse students
    students = {}
    for s in resources.get('students', []):
        students[s['id']] = Student(
            id=s['id'],
            name=s['name'],
            batch=s['batch'],
            semester=s['semester'],
            registered_courses=s['registered_courses'],
            needs_mentor=s['needs_mentor'],
            special_requirements=s.get('special_requirements', [])
        )
    
    # Parse courses
    courses = {}
    for c in resources.get('courses', []):
        courses[c['id']] = Course(
            id=c['id'],
            code=c['code'],
            name=c['name'],
            credits=c['credits'],
            hours_per_week=c['hours_per_week'],
            sessions_per_week=c['sessions_per_week'],
            session_duration=c['session_duration'],
            requires_lab=c['requires_lab'],
            preferred_rooms=c['preferred_rooms'],
            eligible_teachers=c['eligible_teachers'],
            student_groups=c['student_groups']
        )
    
    # Parse rooms
    rooms = {}
    for r in resources.get('rooms', []):
        rooms[r['id']] = Room(
            id=r['id'],
            name=r['name'],
            type=r['type'],
            capacity=r['capacity'],
            facilities=r['facilities'],
            building=r['building'],
            floor=r['floor']
        )
    
    # Parse time slots
    time_slots = {}
    for ts in resources.get('time_slots', []):
        time_slots[ts['id']] = TimeSlot(
            id=ts['id'],
            day=ts['day'],
            start_time=ts['start_time'],
            end_time=ts['end_time'],
            type=ts['type']
        )
    
    # Parse student groups
    student_groups = {}
    for sg in resources.get('student_groups', []):
        student_groups[sg['id']] = StudentGroup(
            id=sg['id'],
            name=sg['name'],
            students=sg['students'],
            courses=sg['courses']
        )
    
    # Parse constraints
    hard_constraints = []
    soft_constraints = []
    
    for c in data.get('constraints', {}).get('hard_constraints', []):
        hard_constraints.append(Constraint(
            type=c['type'],
            description=c['description'],
            weight=c['weight']
        ))
    
    for c in data.get('constraints', {}).get('soft_constraints', []):
        soft_constraints.append(Constraint(
            type=c['type'],
            description=c['description'],
            weight=c['weight']
        ))
    
    return {
        'teachers': teachers,
        'students': students,
        'courses': courses,
        'rooms': rooms,
        'time_slots': time_slots,
        'student_groups': student_groups,
        'hard_constraints': hard_constraints,
        'soft_constraints': soft_constraints,
        'algorithm_parameters': data.get('algorithm_parameters', {})
    }

def save_timetable(timetable: Dict[str, Any], file_path: str) -> None:
    """
    Save generated timetable to JSON file.
    """
    # Convert complex objects to serializable format
    serializable_timetable = {
        'assignments': []
    }
    
    for course_id, assignment in timetable.items():
        serializable_timetable['assignments'].append({
            'course_id': course_id,
            'teacher_id': assignment['teacher_id'],
            'room_id': assignment['room_id'],
            'time_slot_id': assignment['time_slot_id']
        })
    
    with open(file_path, 'w') as f:
        json.dump(serializable_timetable, f, indent=2)

def visualize_timetable(timetable: Dict[str, Any], data: Dict[str, Any] = None) -> None:
    """
    Visualize timetable as a heatmap by teacher and day/time.
    """
    if not data:
        print("Warning: Data not provided for visualization, using placeholder values")
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        time_periods = ["09:00-10:00", "10:00-11:00", "11:00-12:00", "12:00-13:00", "14:00-15:00"]
        teachers = [f"T{i}" for i in range(1, 7)]
    else:
        # Extract days and time periods from data
        time_slots = list(data['time_slots'].values())
        days = sorted(list(set([ts.day for ts in time_slots])))
        time_periods = sorted(list(set([f"{ts.start_time}-{ts.end_time}" for ts in time_slots])))
        teachers = list(data['teachers'].keys())
    
    # Create figure for teacher view
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_title("Timetable by Teacher and Time")
    
    # Create a matrix for visualization (Teacher x (Day, Period))
    matrix = np.zeros((len(teachers), len(days) * len(time_periods)))
    matrix.fill(np.nan)  # Set all to NaN for empty cells
    
    # Fill the matrix based on timetable
    for course_id, assignment in timetable.items():
        teacher_id = assignment['teacher_id']
        time_slot_id = assignment['time_slot_id']
        
        if data:
            time_slot = data['time_slots'][time_slot_id]
            day_idx = days.index(time_slot.day)
            period_idx = time_periods.index(f"{time_slot.start_time}-{time_slot.end_time}")
            teacher_idx = teachers.index(teacher_id)
        else:
            # For placeholder visualization
            day_idx = random.randint(0, len(days) - 1)
            period_idx = random.randint(0, len(time_periods) - 1)
            teacher_idx = random.randint(0, len(teachers) - 1)
        
        cell_idx = day_idx * len(time_periods) + period_idx
        matrix[teacher_idx, cell_idx] = 1  # Mark as assigned
    
    # Create colormap with NaN handling
    cmap = plt.cm.YlOrRd
    cmap.set_bad('white', 1.)
    
    # Create the heatmap
    im = ax.imshow(matrix, cmap=cmap)
    
    # Set labels
    ax.set_xlabel("Day and Period")
    ax.set_ylabel("Teacher")
    
    # Set ticks
    ax.set_yticks(np.arange(len(teachers)))
    ax.set_yticklabels(teachers)
    
    # Create composite labels for x-axis
    x_labels = []
    for day in days:
        for period in time_periods:
            x_labels.append(f"{day[:3]} {period}")
    
    # Set x-ticks every 5 positions to avoid overcrowding
    tick_positions = np.arange(0, len(days) * len(time_periods), 5)
    ax.set_xticks(tick_positions)
    ax.set_xticklabels([x_labels[pos] for pos in tick_positions], rotation=45, ha="right")
    
    # Add colorbar
    cbar = plt.colorbar(im)
    cbar.set_label('Assignment')
    
    plt.tight_layout()
    plt.savefig("timetable_visualization.png")
    plt.show()

def calculate_constraint_violations(timetable: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, int]:
    """
    Calculate violations of constraints in a timetable.
    Returns a dictionary with constraint types as keys and violation counts as values.
    """
    violations = {
        "teacher_overlap": 0,
        "room_overlap": 0,
        "mentor_group_size": 0,
        "back_to_back_sessions": 0,
        "equitable_teaching_load": 0
    }
    
    # Check for teacher overlaps (no teacher scheduled for multiple classes at once)
    teacher_assignments = {}
    for course_id, assignment in timetable.items():
        teacher_id = assignment['teacher_id']
        time_slot_id = assignment['time_slot_id']
        
        if teacher_id not in teacher_assignments:
            teacher_assignments[teacher_id] = []
        
        teacher_assignments[teacher_id].append(time_slot_id)
    
    # Count overlapping time slots for each teacher
    for teacher_id, time_slots in teacher_assignments.items():
        for i, ts1_id in enumerate(time_slots):
            ts1 = data['time_slots'][ts1_id]
            for ts2_id in time_slots[i+1:]:
                ts2 = data['time_slots'][ts2_id]
                if ts1.overlaps_with(ts2):
                    violations["teacher_overlap"] += 1
    
    # Check for room overlaps (no room used for multiple classes at once)
    room_assignments = {}
    for course_id, assignment in timetable.items():
        room_id = assignment['room_id']
        time_slot_id = assignment['time_slot_id']
        
        if room_id not in room_assignments:
            room_assignments[room_id] = []
        
        room_assignments[room_id].append(time_slot_id)
    
    # Count overlapping time slots for each room
    for room_id, time_slots in room_assignments.items():
        for i, ts1_id in enumerate(time_slots):
            ts1 = data['time_slots'][ts1_id]
            for ts2_id in time_slots[i+1:]:
                ts2 = data['time_slots'][ts2_id]
                if ts1.overlaps_with(ts2):
                    violations["room_overlap"] += 1
    
    # Check mentor group size (each mentor should have exactly 4 students)
    mentor_students = {}
    for teacher_id, teacher in data['teachers'].items():
        if teacher.is_mentor:
            mentor_students[teacher_id] = []
    
    # Assign students to mentors based on course assignments
    for course_id, assignment in timetable.items():
        teacher_id = assignment['teacher_id']
        if teacher_id in mentor_students:
            course = data['courses'][course_id]
            for group_id in course.student_groups:
                student_group = data['student_groups'][group_id]
                mentor_students[teacher_id].extend(student_group.students)
    
    # Check if each mentor has exactly 4 students
    for teacher_id, students in mentor_students.items():
        # Remove duplicates (students may be in multiple courses)
        unique_students = set(students)
        if len(unique_students) != 4:  # The paper specifies 4 students per mentor
            violations["mentor_group_size"] += abs(len(unique_students) - 4)
    
    # Check for back-to-back sessions (soft constraint)
    for teacher_id, time_slots in teacher_assignments.items():
        # Group time slots by day
        day_slots = {}
        for ts_id in time_slots:
            ts = data['time_slots'][ts_id]
            if ts.day not in day_slots:
                day_slots[ts.day] = []
            day_slots[ts.day].append(ts)
        
        # Check for back-to-back sessions on each day
        for day, slots in day_slots.items():
            slots.sort(key=lambda ts: ts.start_time)
            for i in range(len(slots) - 1):
                end_time_1 = slots[i]._time_to_minutes(slots[i].end_time)
                start_time_2 = slots[i+1]._time_to_minutes(slots[i+1].start_time)
                if start_time_2 - end_time_1 == 0:  # Back-to-back sessions
                    violations["back_to_back_sessions"] += 1
    
    # Check for equitable teaching load (soft constraint)
    teaching_load = {teacher_id: 0 for teacher_id in data['teachers']}
    for course_id, assignment in timetable.items():
        teacher_id = assignment['teacher_id']
        course = data['courses'][course_id]
        teaching_load[teacher_id] += course.hours_per_week
    
    # Calculate standard deviation of teaching loads
    if teaching_load:
        loads = list(teaching_load.values())
        mean_load = sum(loads) / len(loads)
        variance = sum((load - mean_load) ** 2 for load in loads) / len(loads)
        std_dev = variance ** 0.5
        
        # Scale the standard deviation to get a meaningful violation count
        violations["equitable_teaching_load"] = int(std_dev * 10)
    
    return violations
