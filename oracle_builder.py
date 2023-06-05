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