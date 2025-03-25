A System for Automating Timetable Generation
![GitHub license](https://img.shields.io/badge/license-MIT-blue.g.shields.io/badge/python-3.img.shields.io/badge/stat](https://img.shields.io/badge/version-1.0.0-brightgr system for automatically generating academic timetables by optimizing multiple constraints using advanced algorithms including Genetic Algorithms, Simulated Annealing, and Constraint Programming.

📑 Table of Contents
Overview

Features

Installation

Usage

Algorithms Implemented

Project Structure

Experimental Results

Technologies Used

Contributors

License

Citation

📚 Overview
The generation of academic timetables is a complex and time-consuming task that requires balancing multiple constraints, such as the availability of teachers, students, and classrooms, as well as minimizing schedule conflicts. This system automates timetable generation through the application of various optimization algorithms, efficiently allocating resources while adhering to conditions like:

Assigning mentors to a fixed number of students

Ensuring teachers do not take back-to-back sessions

Optimizing room utilization

Distributing teaching load equitably

Through a combination of constraint satisfaction, genetic algorithms, and optimization methods, the proposed system generates feasible timetables while ensuring flexibility and scalability.

✨ Features
Multiple Algorithm Implementations:

Genetic Algorithms (GA)

Simulated Annealing (SA)

Constraint Programming (CP)

Hybrid GA-SA approach

Constraint Handling:

Avoids teacher schedule conflicts

Prevents room double-booking

Manages mentor-student group assignments

Optimizes teaching load distribution

Flexible Configuration:

Adjustable parameters for each algorithm

Customizable constraints and priorities

Scalable for different institution sizes

Performance Optimization:

Efficient search space exploration

Parallel processing capabilities

Convergence acceleration techniques

🔧 Installation
bash
# Clone the repository
git clone https://github.com/SohamDutta2002/A-System-for-Automating-TimeTable-Generation.git

# Navigate to the project directory
cd A-System-for-Automating-TimeTable-Generation

# Install dependencies
pip install -r requirements.txt
🚀 Usage
python
# Example usage code
from timetable_generator import TimetableGenerator

# Initialize the generator with parameters
generator = TimetableGenerator(
    teachers=teachers_list,
    courses=courses_list,
    rooms=rooms_list,
    timeslots=timeslots_list,
    algorithm="hybrid"  # Options: "genetic", "simulated_annealing", "constraint", "hybrid"
)

# Generate the timetable
timetable = generator.generate()

# Export the results
generator.export_timetable(timetable, format="csv")
🧠 Algorithms Implemented
Genetic Algorithm (GA)
The GA implementation uses:

Chromosome representation for timetable solutions

Selection mechanisms for parent solutions

Crossover and mutation operators

Fitness function evaluating constraint violations

Simulated Annealing (SA)
The SA implementation includes:

Initial solution generation

Neighbor generation mechanisms

Temperature cooling schedules (geometric and logarithmic)

Probabilistic acceptance criteria

Constraint Programming (CP)
The CP approach utilizes:

Variable and constraint definition

Constraint propagation techniques

Backtracking search algorithms

Objective function optimization

Hybrid GA-SA Algorithm
The hybrid approach combines:

GA's global search capabilities

SA's local search refinement

Adaptive parameter adjustment

Enhanced constraint handling

📁 Project Structure
text
├── src/
│   ├── algorithms/
│   │   ├── genetic_algorithm.py
│   │   ├── simulated_annealing.py
│   │   ├── constraint_programming.py
│   │   └── hybrid_algorithm.py
│   ├── models/
│   │   ├── timetable.py
│   │   ├── teacher.py
│   │   ├── course.py
│   │   └── room.py
│   ├── utils/
│   │   ├── data_loader.py
│   │   ├── constraint_validator.py
│   │   └── export_utils.py
│   └── main.py
├── data/
│   ├── teachers.csv
│   ├── courses.csv
│   └── rooms.csv
├── tests/
│   ├── test_genetic_algorithm.py
│   ├── test_simulated_annealing.py
│   └── test_hybrid_algorithm.py
├── examples/
│   ├── basic_usage.py
│   └── advanced_configuration.py
├── docs/
│   ├── algorithms.md
│   ├── constraints.md
│   └── configuration.md
├── README.md
├── requirements.txt
└── LICENSE
📊 Experimental Results
Our experimental validation demonstrates:

Faster convergence (20-30% reduction in execution time)

Higher solution quality (approximately 40% improvement in constraint satisfaction)

Near-linear scalability for larger datasets

In our initial implementation with a simplified dataset (6 teachers, 5 courses, 4 rooms, and 5 timeslots), the hybrid algorithm converged to a fitness value of -12 after 500 generations, representing significant conflict resolution compared to the initial random population.

🛠️ Technologies Used
Python 3.8+

NumPy for numerical computations

DEAP library for genetic algorithms

SimAnneal for simulated annealing implementations

OR-Tools for constraint programming

Multiprocessing for parallel execution

👥 Contributors
Arkaprabha Bera - 2151141

Rupam Nandi - 2151142

Soham Dutta - 2151146

Akanksh Kumar Shaw - 2151226

Mentors:

Prof. Subhasis Majumdar

Prof. Subhajit Dutta

Department of Computer Science and Engineering, Heritage Institute of Technology

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

📝 Citation
If you use this system in your research or project, please cite:

text
@article{bera2023system,
  title={A System for Automating TimeTable Generation},
  author={Bera, Arkaprabha and Nandi, Rupam and Dutta, Soham and Shaw, Akanksh Kumar},
  journal={Department of Computer Science and Engineering, Heritage Institute of Technology},
  year={2023}
}