# Oracle Builder Project

The goal of this project is to practice my Qiskit skills. To do this, I'll be writing a script that can take a given string of bits (for example '100101') and does the following:
- Build an oracle for which the given bit string is the answer.
- Find that answer using Grover's algorithm.

To launch the application, simply run the command `python3 main.py` in a console open inside the project directory. You'll be asked to enter a 1s and 0s bit string, or to press ENTER to exit the program.

## Dependencies

This project was built with the following packages:
- Python (3.11.3)
- qiskit-terra (0.24.0)
- qiskit-aer (0.12.0)