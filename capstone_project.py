# ==============================================================================
# FILE: capstone_project.py
# ==============================================================================
# Capstone project
# This file provides functions to create quantum circuits that execute Grover's
# algorithm.
# Learners are expected to implement the logic for the `four_qubit_grover`
# function within the specified section of the function.
#
# Instructions:
# - Complete the `four_qubit_grover` function as described in its docstring.
# - Do not modify code outside the indicated editable section.
# - You are only allowed to to use the Hadamard gate, the X gate and the
#   multi controlled X gate.
#
# Testing:
# - To verify your implementation, run the provided test file:
#   test_capstone_project.py,  using the command:
#   python -m unittest test_capstone_project.py
# ------------------------------------------------------------------------------
from qiskit import QuantumCircuit


def two_qubit_grover_11() -> QuantumCircuit:
    """
    This function creates and returns a quantum circuit that performs Grover's
    algorithm for 2 qubits for the solution 11. It does not measure the circuit.

    :returns:   The quantum circuit that runs Grover's algorithm for 2 qubits
                with the solution 11.
    :rtype:     QuantumCircuit
    """
    ############
    # DO NOT EDIT THIS FUNCTION
    num_qubits = 2
    qc = QuantumCircuit(num_qubits)

    # Step 1: Initialise
    qc.h(range(num_qubits))

    # Step 2: Tag solution
    qc.cz(0, 1)

    # Step 3: Grover diffusion
    qc.h(range(num_qubits))
    qc.x(range(num_qubits))
    qc.cz(0, 1)
    qc.x(range(num_qubits))
    qc.h(range(num_qubits))

    return qc


def four_qubit_grover(solution: str) -> QuantumCircuit:
    """
    This function creates and returns a quantum circuit that performs Grover's algorithm for 4 qubits
    for any given solution string (e.g., "0010"). It does not measure the circuit.

    :param solution:    4-bit string representing the solution to mark (e.g., "0010")
    :type solution:     str
    :returns:           Quantum circuit running Grover's algorithm for 4 qubits with the given solution.
    :rtype:             QuantumCircuit
    """
    num_qubits = 4
    qc = QuantumCircuit(num_qubits)
    ############
    # ONLY EDIT UNDER HERE
    qc.h(range(num_qubits))
    last = num_qubits - 1
    for _ in range(3):
        for i, bit in enumerate(solution):
            if bit == '0':
                qc.x(i)
        qc.h(last)
        qc.mcx(list(range(num_qubits - 1)), last)
        qc.h(last)
        for i, bit in enumerate(solution):
            if bit == '0':
                qc.x(i)
        qc.h(range(num_qubits))
        qc.x(range(num_qubits))
        qc.h(last)
        qc.mcx(list(range(num_qubits - 1)), last)
        qc.h(last)
        qc.x(range(num_qubits))
        qc.h(range(num_qubits))

    # ONLY EDIT ABOVE HERE
    ######
    return qc
