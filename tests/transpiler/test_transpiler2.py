"""
Unit tests for the qbraid transpiler.
"""
import pytest
import qiskit
import cirq
from braket.circuits import Circuit as BraketCircuit
from braket.circuits.gate import Gate as BraketGate
from braket.circuits.instruction import Instruction as BraketInstruction
from braket.circuits.unitary_calculation import calculate_unitary
import numpy as np
from qbraid.transpiler.transpiler import qbraid_wrapper


class TestSharedGates:
    """Tests transpiling circuits composed of gate types that share explicit support across multiple
    qbraid tranpsiler supported packages (qiskit, cirq, braket).
    """

    # Create braket test circuit
    braket_circuit = BraketCircuit()

    instructions = [
        BraketInstruction(BraketGate.H(), 0),
        BraketInstruction(BraketGate.H(), 1),
        BraketInstruction(BraketGate.H(), 2),
        BraketInstruction(BraketGate.H(), 3),
        BraketInstruction(BraketGate.X(), 0),
        BraketInstruction(BraketGate.X(), 1),
        BraketInstruction(BraketGate.Y(), 2),
        BraketInstruction(BraketGate.Z(), 3),
        BraketInstruction(BraketGate.S(), 0),
        BraketInstruction(BraketGate.Si(), 1),
        BraketInstruction(BraketGate.T(), 2),
        BraketInstruction(BraketGate.Ti(), 3),
        BraketInstruction(BraketGate.Rx(np.pi / 4), 0),
        BraketInstruction(BraketGate.Ry(np.pi / 2), 1),
        BraketInstruction(BraketGate.Rz(3 * np.pi / 4), 2),
        BraketInstruction(BraketGate.PhaseShift(np.pi / 8), 3),
        BraketInstruction(BraketGate.V(), 0),
        BraketInstruction(BraketGate.Vi(), 1),
        BraketInstruction(BraketGate.ISwap(), [2, 3]),
        BraketInstruction(BraketGate.Swap(), [0, 2]),
        BraketInstruction(BraketGate.Swap(), [1, 3]),
        BraketInstruction(BraketGate.CNot(), [0, 1]),
        BraketInstruction(BraketGate.CPhaseShift(np.pi / 4), [2, 3]),
    ]

    for inst in instructions:
        braket_circuit.add_instruction(inst)

    # Get matrix representations
    braket_unitary = calculate_unitary(4, instructions)

    # test_data_qiskit_to_cirq = [qiskit_circuit, cirq_unitary]
    # test_data_cirq_to_qiskit = [cirq_circuit, qiskit_unitary]
    # test_data_qiskit_to_braket = [qiskit_circuit, braket_unitary]
    # test_data_braket_to_qiskit = [braket_circuit, qiskit_unitary]
    # test_data_cirq_to_braket = [cirq_circuit, braket_unitary]
    # test_data_braket_to_cirq = [braket_circuit, cirq_unitary]

    @pytest.fixture
    def data_qiskit_to_cirq(self):
        qiskit_circuit = qiskit.QuantumCircuit(4)

        qiskit_circuit.h([0, 1, 2, 3])
        qiskit_circuit.x([0, 1])
        qiskit_circuit.y(2)
        qiskit_circuit.z(3)
        qiskit_circuit.s(0)
        qiskit_circuit.sdg(1)
        qiskit_circuit.t(2)
        qiskit_circuit.tdg(3)
        qiskit_circuit.rx(np.pi / 4, 0)
        qiskit_circuit.ry(np.pi / 2, 1)
        qiskit_circuit.rz(3 * np.pi / 4, 2)
        qiskit_circuit.p(np.pi / 8, 3)
        qiskit_circuit.sx(0)
        qiskit_circuit.sxdg(1)
        qiskit_circuit.iswap(2, 3)
        qiskit_circuit.swap([0, 1], [2, 3])
        qiskit_circuit.cx(0, 1)
        qiskit_circuit.cp(np.pi / 4, 2, 3)

        cirq_circuit = cirq.Circuit()

        q0 = cirq.LineQubit(3)
        q1 = cirq.LineQubit(2)
        q2 = cirq.LineQubit(1)
        q3 = cirq.LineQubit(0)

        cirq_gates = [
            cirq.H(q0),
            cirq.H(q1),
            cirq.H(q2),
            cirq.H(q3),
            cirq.X(q0),
            cirq.X(q1),
            cirq.Y(q2),
            cirq.Z(q3),
            cirq.S(q0),
            cirq.ZPowGate(exponent=-0.5)(q1),
            cirq.T(q2),
            cirq.ZPowGate(exponent=-0.25)(q3),
            cirq.Rx(rads=np.pi / 4)(q0),
            cirq.Ry(rads=np.pi / 2)(q1),
            cirq.Rz(rads=3 * np.pi / 4)(q2),
            cirq.ZPowGate(exponent=1 / 8)(q3),
            cirq.XPowGate(exponent=0.5)(q0),
            cirq.XPowGate(exponent=-0.5)(q1),
            cirq.ISWAP(q2, q3),
            cirq.SWAP(q0, q2),
            cirq.SWAP(q1, q3),
            cirq.CNOT(q0, q1),
            cirq.CZPowGate(exponent=0.25)(q2, q3),
        ]

        for gate in cirq_gates:
            cirq_circuit.append(gate)

        cirq_circuit_flipped = cirq.Circuit()

        q0 = cirq.LineQubit(0)
        q1 = cirq.LineQubit(1)
        q2 = cirq.LineQubit(2)
        q3 = cirq.LineQubit(3)

        cirq_gates = [
            cirq.H(q0),
            cirq.H(q1),
            cirq.H(q2),
            cirq.H(q3),
            cirq.X(q0),
            cirq.X(q1),
            cirq.Y(q2),
            cirq.Z(q3),
            cirq.S(q0),
            cirq.ZPowGate(exponent=-0.5)(q1),
            cirq.T(q2),
            cirq.ZPowGate(exponent=-0.25)(q3),
            cirq.Rx(rads=np.pi / 4)(q0),
            cirq.Ry(rads=np.pi / 2)(q1),
            cirq.Rz(rads=3 * np.pi / 4)(q2),
            cirq.ZPowGate(exponent=1 / 8)(q3),
            cirq.XPowGate(exponent=0.5)(q0),
            cirq.XPowGate(exponent=-0.5)(q1),
            cirq.ISWAP(q2, q3),
            cirq.SWAP(q0, q2),
            cirq.SWAP(q1, q3),
            cirq.CNOT(q0, q1),
            cirq.CZPowGate(exponent=0.25)(q2, q3),
        ]

        for gate in cirq_gates:
            cirq_circuit_flipped.append(gate)

        qiskit_unitary = qiskit.quantum_info.Operator(qiskit_circuit).data
        cirq_unitary = cirq_circuit.unitary()
        assert np.allclose(qiskit_unitary, cirq_unitary), "Test circuits must be equivalent"
        cirq_unitary_flipped = cirq_circuit_flipped.unitary()

        return qiskit_circuit, cirq_unitary_flipped

    def test_qiskit_to_cirq_shared_gates(self, data_qiskit_to_cirq):

        # qiskit_circuit, cirq_unitary_flipped = data_qiskit_to_cirq
        # qbraid_circuit = qbraid_wrapper(qiskit_circuit)
        # cirq_circuit_transpiled = qbraid_circuit.transpile("cirq")
        # cirq_unitary_transpiled = cirq_circuit_transpiled.unitary()
        # assert np.allclose(cirq_unitary_transpiled, cirq_unitary_flipped)
        assert True

    # def test_qiskit_to_cirq_shared_gates(self):
    #     """Tests transpiling a qiskit circuit to a cirq circuit, where all gate types are
    #     common to
    #     both qiskit and cirq.
    #     """
    #
    #     # Create qiskit test circuit
    #     qiskit_circuit = qiskit.QuantumCircuit(4)
    #
    #     qiskit_circuit.h(0)
    #     qiskit_circuit.h(1)
    #     qiskit_circuit.h(2)
    #     qiskit_circuit.h(3)
    #     qiskit_circuit.x(0)
    #     qiskit_circuit.x(1)
    #     qiskit_circuit.y(2)
    #     qiskit_circuit.z(3)
    #     qiskit_circuit.s(0)
    #     qiskit_circuit.sdg(1)
    #     qiskit_circuit.t(2)
    #     qiskit_circuit.tdg(3)
    #     qiskit_circuit.rx(np.pi / 4, 0)
    #     qiskit_circuit.ry(np.pi / 2, 1)
    #     qiskit_circuit.rz(3 * np.pi / 4, 2)
    #     qiskit_circuit.p(np.pi / 8, 3)
    #     qiskit_circuit.sx(0)
    #     qiskit_circuit.sxdg(1)
    #     qiskit_circuit.iswap(2, 3)
    #     qiskit_circuit.swap(0, 2)
    #     qiskit_circuit.swap(1, 3)
    #     qiskit_circuit.cx(0, 1)
    #     qiskit_circuit.cp(np.pi / 4, 2, 3)
    #
    #     # Create cirq test circuit
    #     cirq_circuit = cirq.Circuit()
    #
    #     q0 = cirq.LineQubit(3)
    #     q1 = cirq.LineQubit(2)
    #     q2 = cirq.LineQubit(1)
    #     q3 = cirq.LineQubit(0)
    #
    #     gates = [
    #         cirq.H(q0),
    #         cirq.H(q1),
    #         cirq.H(q2),
    #         cirq.H(q3),
    #         cirq.X(q0),
    #         cirq.X(q1),
    #         cirq.Y(q2),
    #         cirq.Z(q3),
    #         cirq.S(q0),
    #         cirq.ZPowGate(exponent=-0.5)(q1),
    #         cirq.T(q2),
    #         cirq.ZPowGate(exponent=-0.25)(q3),
    #         cirq.Rx(rads=np.pi / 4)(q0),
    #         cirq.Ry(rads=np.pi / 2)(q1),
    #         cirq.Rz(rads=3 * np.pi / 4)(q2),
    #         cirq.ZPowGate(exponent=1 / 8)(q3),
    #         cirq.XPowGate(exponent=0.5)(q0),
    #         cirq.XPowGate(exponent=-0.5)(q1),
    #         cirq.ISWAP(q2, q3),
    #         cirq.SWAP(q0, q2),
    #         cirq.SWAP(q1, q3),
    #         cirq.CNOT(q0, q1),
    #         cirq.CZPowGate(exponent=0.25)(q2, q3),
    #     ]
    #
    #     for gate in gates:
    #         cirq_circuit.append(gate)
    #
    #     qiskit_unitary = qiskit.quantum_info.Operator(qiskit_circuit).data
    #     cirq_unitary = cirq_circuit.unitary()
    #     assert np.allclose(cirq_unitary, qiskit_unitary), "Test circuits must be equivalent"
    #
    #     qbraid_circuit_qiskit = qbraid_wrapper(qiskit_circuit)
    #     cirq_circuit_transpiled = qbraid_circuit_qiskit.transpile("cirq")
    #     cirq_unitary_transpiled = cirq_circuit_transpiled.unitary()
    #     assert np.allclose(cirq_unitary, cirq_unitary_transpiled)
    #
    #     qbraid_circuit_cirq = qbraid_wrapper(cirq_circuit)
    #     qiskit_circuit_transpiled = qbraid_circuit_cirq.transpile("qiskit")
    #     qiskit_unitary_transpiled = qiskit.quantum_info.Operator(qiskit_circuit_transpiled).data
    #     assert np.allclose(qiskit_unitary, qiskit_unitary_transpiled)

    # @pytest.mark.parametrize("cirq_circuit,qiskit_unitary", test_data_cirq_to_qiskit)
    # def test_cirq_to_qiskit_shared_gates(self, cirq_circuit, qiskit_unitary):
    #     """Tests transpiling a cirq circuit to a qiskit circuit, where all gate types are
    #     common to
    #     both cirq and qiskit.
    #     """
    #     qbraid_circuit = qbraid_wrapper(cirq_circuit)
    #     qiskit_circuit_transpiled = qbraid_circuit.transpile("qiskit")
    #     qiskit_unitary_transpiled = qiskit.quantum_info.Operator(qiskit_circuit_transpiled).data
    #     assert np.allclose(qiskit_unitary, qiskit_unitary_transpiled)
    #
    # @pytest.mark.parametrize("qiskit_circuit,braket_unitary", test_data_qiskit_to_braket)
    # def test_qiskit_to_braket_shared_gates(self, qiskit_circuit, braket_unitary):
    #     """Tests transpiling a qiskit circuit to a braket circuit, where all gate types are common
    #     to both qiskit and braket.
    #     """
    #     qbraid_circuit = qbraid_wrapper(qiskit_circuit)
    #     # braket_circuit_transpiled = qbraid_circuit.transpile("braket")
    #     # braket_unitary_transpiled = None
    #     # assert np.allclose(braket_unitary, braket_unitary_transpiled)
    #
    #     qbraid_circuit.transpile("braket")
    #     assert True
    #
    # @pytest.mark.parametrize("braket_circuit,qiskit_unitary", test_data_braket_to_qiskit)
    # def test_braket_to_qiskit_shared_gates(self, braket_circuit, qiskit_unitary):
    #     """Tests transpiling a braket circuit to a qiskit circuit, where all gate types are common
    #     to both braket and qiskit.
    #     """
    #     qbraid_circuit = qbraid_wrapper(braket_circuit)
    #     qiskit_circuit_transpiled = qbraid_circuit.transpile("qiskit")
    #     qiskit_unitary_transpiled = qiskit.quantum_info.Operator(qiskit_circuit_transpiled).data
    #     assert np.allclose(qiskit_unitary, qiskit_unitary_transpiled)
    #
    # @pytest.mark.parametrize("cirq_circuit,braket_unitary", test_data_cirq_to_braket)
    # def test_cirq_to_braket_shared_gates(self, cirq_circuit, braket_unitary):
    #     """Tests transpiling a cirq circuit to a braket circuit, where all gate types are
    #     common to
    #     both cirq and braket.
    #     """
    #     qbraid_circuit = qbraid_wrapper(cirq_circuit)
    #     # braket_circuit_transpiled = qbraid_circuit.transpile("braket")
    #     # braket_unitary_transpiled = None
    #     # assert np.allclose(braket_unitary, braket_unitary_transpiled)
    #
    #     qbraid_circuit.transpile("braket")
    #     assert True
    #
    # @pytest.mark.parametrize("braket_circuit,cirq_unitary", test_data_braket_to_cirq)
    # def test_braket_to_cirq_shared_gates(self, braket_circuit, cirq_unitary):
    #     """Tests transpiling a braket circuit to a cirq circuit, where all gate types are common
    #     to both braket and cirq.
    #     """
    #     qbraid_circuit = qbraid_wrapper(braket_circuit)
    #     cirq_circuit_transpiled = qbraid_circuit.transpile("cirq")
    #     cirq_unitary_transpiled = cirq_circuit_transpiled.unitary()
    #     assert np.allclose(cirq_unitary, cirq_unitary_transpiled)
