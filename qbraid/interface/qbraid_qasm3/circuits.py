# Copyright (C) 2023 qBraid
#
# This file is part of the qBraid-SDK
#
# The qBraid-SDK is free software released under the GNU General Public License v3
# or later. You can redistribute and/or modify it under the terms of the GPL v3.
# See the LICENSE file in the project root or <https://www.gnu.org/licenses/gpl-3.0.html>.
#
# THERE IS NO WARRANTY for the qBraid-SDK, as per Section 15 of the GPL v3.

"""
Module containing qasm programs used for testing

"""
from typing import Optional

import numpy as np

from qbraid.exceptions import QbraidError

QASMType = str


def create_gateset_qasm(max_operands) -> np.ndarray:
    """gets qasm for gateset with max_operands"""

    q1_gates = [
        ("id", 1, 0),
        ("x", 1, 0),
        ("y", 1, 0),
        ("z", 1, 0),
        ("h", 1, 0),
        ("s", 1, 0),
        ("t", 1, 0),
        ("sdg", 1, 0),
        ("tdg", 1, 0),
        ("sx", 1, 0),
        ("rx", 1, 1),
        ("ry", 1, 1),
        ("rz", 1, 1),
        ("p", 1, 1),
        ("u1", 1, 1),
        ("u2", 1, 2),
        ("u3", 1, 3),
        ("reset", 1, 0),
    ]

    q2_gates = [
        ("cx", 2, 0),
        ("cy", 2, 0),
        ("cz", 2, 0),
        ("ch", 2, 0),
        ("cp", 2, 1),
        ("crx", 2, 1),
        ("cry", 2, 1),
        ("crz", 2, 1),
        ("swap", 2, 0),
        ("cu", 2, 4),
    ]

    q3_gates = [("ccx", 3, 0), ("cswap", 3, 0)]

    gates = q1_gates.copy()

    if max_operands >= 2:
        gates.extend(q2_gates)
    if max_operands >= 3:
        gates.extend(q3_gates)
    gates = np.array(
        gates, dtype=[("gate", object), ("num_qubits", np.int64), ("num_params", np.int64)]
    )
    return gates


def _qasm3_random(
    num_qubits: Optional[int] = None,
    depth: Optional[int] = None,
    max_operands: Optional[int] = None,
    seed=None,
    measure=False,
) -> QASMType:
    """Generate random QASM3 circuit string.

    Args:
        num_qubits (int): number of quantum wires
        depth (int): layers of operations (i.e. critical path length)
        max_operands (int): maximum size of gate for each operation
        seed (int): seed for random number generator
        measure (bool): whether to include measurement gates

    Raises:
        QbraidError: When invalid  random circuit options given

    Returns:
        QASM3 random circuit string

    """

    num_qubits = np.random.randint(1, 4) if num_qubits is None else num_qubits
    depth = np.random.randint(1, 4) if depth is None else depth
    max_operands = np.random.randint(1, 3) if max_operands is None else max_operands
    try:
        if seed is None:
            seed = np.random.randint(0, np.iinfo(np.int32).max)
        np.random.seed(seed)
        rng = np.random.default_rng(seed)
        # create random circuit qasm3.0
        qasm_code_header = f"""
// Random Circuit generated by qBraid
OPENQASM 3.0;
include "stdgates.inc";
/*
    seed = {seed}
    num_qubits = {num_qubits}
    depth = {depth}
    max_operands = {max_operands}
*/
"""
        max_operands = min(max_operands, num_qubits)
        if num_qubits == 0:
            rand_circuit = qasm_code_header
            return rand_circuit
        rand_circuit = qasm_code_header + f"qubit[{num_qubits}] q;\n"
        if measure:
            rand_circuit += f"bit[{num_qubits}] c;\n"
        qubits = np.arange(num_qubits)
        gates = create_gateset_qasm(max_operands)
        for _ in range(depth):
            gate_specs = rng.choice(gates, size=num_qubits)
            cumulative_qubits = np.cumsum(gate_specs["num_qubits"], dtype=np.int64)

            max_index = np.searchsorted(cumulative_qubits, num_qubits, side="right")
            gate_specs = gate_specs[:max_index]
            slack = num_qubits - cumulative_qubits[max_index - 1]
            if slack:
                gates = create_gateset_qasm(max_operands=1)
                slack_gates = rng.choice(gates, size=slack)
                gate_specs = np.hstack((gate_specs, slack_gates))

            q_indices = np.empty(len(gate_specs) + 1, dtype=np.int64)
            p_indices = np.empty(len(gate_specs) + 1, dtype=np.int64)
            q_indices[0] = p_indices[0] = 0
            np.cumsum(gate_specs["num_qubits"], out=q_indices[1:])
            np.cumsum(gate_specs["num_params"], out=p_indices[1:])
            parameters = rng.uniform(0, 2 * np.pi, size=p_indices[-1])
            for i, (gate, _, p) in enumerate(gate_specs):
                if p:
                    params = ",".join(
                        str(parameters[j]) for j in range(p_indices[i], p_indices[i + 1])
                    )
                    qubit_indices = ",".join(
                        f"q[{qubits[j]}]" for j in range(q_indices[i], q_indices[i + 1])
                    )
                    line = f"{gate}({params}) {qubit_indices};\n"
                    rand_circuit += line
                else:
                    qubit_indices = ",".join(
                        f"q[{qubits[j]}]" for j in range(q_indices[i], q_indices[i + 1])
                    )
                    line = f"{gate} {qubit_indices};\n"
                    rand_circuit += line
            qubits = rng.permutation(qubits)
        if measure:
            for i in range(num_qubits):
                rand_circuit += f"c[{i}] = measure q[{i}];\n"

    except Exception as e:
        raise QbraidError("Could not create Qasm random circuit") from e
    return rand_circuit
