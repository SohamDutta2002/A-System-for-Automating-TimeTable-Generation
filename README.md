# A System for Automating Timetable Generation

[![GitHub license](https://img.shields.io/badge/license-MIT-blue)](LICENSE) 
[![Python 3](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-1.0.0-brightgreen)](https://github.com/SohamDutta2002/A-System-for-Automating-TimeTable-Generation)

A system for automatically generating academic timetables by optimizing multiple constraints using advanced algorithms including Genetic Algorithms, Simulated Annealing, and Constraint Programming.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Algorithms Implemented](#algorithms-implemented)
- [Project Structure](#project-structure)
- [Experimental Results](#experimental-results)
- [Technologies Used](#technologies-used)
- [Contributors](#contributors)
- [License](#license)
- [Citation](#citation)

---

## Overview

Generating academic timetables is a complex, time-consuming task involving multiple constraints such as the availability of teachers, students, and classrooms, along with minimizing schedule conflicts. This system automates timetable generation by efficiently allocating resources while ensuring conditions like:

- Assigning mentors to a fixed number of students
- Avoiding teacher back-to-back sessions
- Optimizing room utilization
- Distributing teaching load equitably

Using a combination of constraint satisfaction, genetic algorithms, and other optimization methods, the system generates feasible timetables that are both flexible and scalable.

---

## Features

- **Multiple Algorithm Implementations:**
  - Genetic Algorithms (GA)
  - Simulated Annealing (SA)
  - Constraint Programming (CP)
  - Hybrid GA-SA Approach

- **Constraint Handling:**
  - Avoids teacher schedule conflicts
  - Prevents room double-booking
  - Manages mentor-student group assignments
  - Optimizes teaching load distribution

- **Flexible Configuration:**
  - Adjustable algorithm parameters
  - Customizable constraints and priorities
  - Scalable for different institution sizes

- **Performance Optimization:**
  - Efficient search space exploration
  - Parallel processing capabilities
  - Convergence acceleration techniques

---

## Installation

Open your terminal and follow these steps:

```bash
# Clone the repository
git clone https://github.com/SohamDutta2002/A-System-for-Automating-TimeTable-Generation.git

# Navigate to the project directory
cd A-System-for-Automating-TimeTable-Generation

# Install dependencies
pip install -r requirements.txt
