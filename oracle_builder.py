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

# Auxiliary function to get multi-cz gate
def build_multi_cz(N):
    '''
    Params:
        N : int
            Amount of qubits to be used in the gate
    Returns:
        Qiskit Gate that acts as a controled z in 
        which the overall phase is multiplied by 
        -1 when all qubits are in state |1>.
    '''
    custom_cz = ZGate().control(N - 1)
    return custom_cz


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
    for i in range(len(bit_string)):
        bit_i = int(bit_string[-1-i])
        # If bit is 0 apply not gate
        if bit_i == 0:
            oracle.x(i)

    # Build custom gate that applies a cz operation on system state
    # when all qubits are in state | 1 >
    custom_cz = build_multi_cz(len(bit_string))
    oracle.append(custom_cz, [i for i in range(len(bit_string))])

    # Reverse encoding logic
    for i in range(len(bit_string)):
        bit_i = int(bit_string[-1-i])
        # If bit is 0 apply not gate
        if bit_i == 0:
            oracle.x(i)
    
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
        Prints the oracle circuit and the best result for the 
        simulation of the circuit. If the oracle circuit is
        correctly built, the results should match the user 
        input exactly.
        Also returns the best result for optional post-processing.
    '''
    # Initialize backend
    backend = Aer.get_backend('aer_simulator')

    # Define list of qubits
    qubits_list = [i for i in range(len(bit_string))]

    # Define initial state
    init_s = QuantumCircuit(len(bit_string))
    init_s.h(qubits_list)

    # Make a copy of the oracle
    qc = oracle.copy()
    # Add measurements to copy 
    qc.measure_all()

    # Build diffuser
    diffuser = QuantumCircuit(len(bit_string))
    diffuser.h(qubits_list)
    diffuser.x(qubits_list)
    custom_cz = build_multi_cz(len(bit_string))
    diffuser.append(custom_cz, qubits_list)
    diffuser.x(qubits_list)
    diffuser.h(qubits_list)


    # Run simulation on the oracle circuit and
    # get counts and unitary matrix
    t_qc = transpile(qc, backend)
    counts = backend.run(t_qc).result().get_counts()
    # Find max result
    best_count = 0 
    best_key = 0
    for key in counts:
        if best_count < counts[key]:
            best_count = counts[key]
            best_key = key

    # Print circuit
    print('\nOracle circuit:')
    print(oracle.draw('text'))
    # Print winner result
    print('Best result:', best_key)
    return best_key