import unittest
import numpy as np
from qiskit.quantum_info import Statevector
from capstone_project import four_qubit_grover


class TestGroversCircuit(unittest.TestCase):
    def test_grovers_circuit_with_solution_0000_returns_solution_state(self):
        expected_values = {
            format(i, "04b"): int(format(i, "04b")[::-1], 2) for i in range(16)
        }
        for bitstring, expected_solution in expected_values.items():
            qc = four_qubit_grover(bitstring)
            state = Statevector.from_instruction(qc)
            probabilities = np.abs(state.data)
            max_prob = np.max(probabilities)
            solution_state = np.argmax(probabilities)
            self.assertEqual(solution_state, expected_solution)
            self.assertTrue(max_prob >= 0.93)

    def test_grover_circuit_contains_only_certain_gates(self):
        expected_values = {
            format(i, "04b"): int(format(i, "04b")[::-1], 2) for i in range(16)
        }
        for bitstring, _ in expected_values.items():
            qc = four_qubit_grover(bitstring)
            allowed_gates = {"h", "x", "mcx"}
            for instr in qc.data:
                self.assertIn(
                    instr.name, allowed_gates, f"Found disallowed gate: {instr.name}"
                )
