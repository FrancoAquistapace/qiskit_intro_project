#Copyright 2023 Franco Aquistapace
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

# This file contains the oracle_builder application

# Import modules
from qiskit import QuantumCircuit, Aer, transpile
from qiskit.circuit.library.standard_gates import ZGate

# Define builder function
def build_oracle_from_string(bit_string):
    '''
    Params:
        bit_string : str
            String containing the bits that act as the solution
            of the oracle.
    Returns:
        QuantumCircuit object that implements the oracle for which
        bit_string is the solution.
    '''
    # Initialize quantum circuit, using as many qubits as needed
    oracle = QuantumCircuit(len(bit_string))

    # We need to apply some logic to build the oracle, so 
    # that its correct answer is given by bit_string

    # Build custom gate that applies a cz operation on system state
    # when all qubits are in state | 1 >
    custom_cz = ZGate().control(len(bit_string) - 1)
    oracle.append(custom_cz, [i for i in range(len(bit_string))])
    
    return oracle


# Define function to run a simulation on the oracle circuit
def run_oracle(oracle, bit_string):
    '''
    Params:
        oracle : QuantumCircuit
            Oracle circuit to be simulated.
        bit_string : str
            String of bits that is the answer to the oracle.
    Returns:
        Prints the oracle circuit and the results for the 
        simulation of the circuit. If the oracle circuit is
        correctly built, the results should match the user 
        input exactly.
        Also returns the resulting unitary matrix for optional 
        post-processing.
    '''
    # Initialize backend
    backend = Aer.get_backend('aer_simulator')
    # Make a copy of the oracle
    qc = oracle.copy()
    # Add measurements to copy 
    qc.measure_all()

    # Run simulation on the oracle circuit and
    # get counts and unitary matrix
    t_qc = transpile(qc, backend)
    counts = backend.run(t_qc).result().get_counts()
    # Find max result
    best_count = 0 
    best_key = 0
    for key in counts.keys:
        if best_count < counts[key]:
            best_count = counts[key]
            best_key = key

    # Print circuit
    print('\nOracle circuit:')
    print(oracle.draw('text'))
    # Print winner result
    print('Best result:', best_key)
    return unitary