from typing import Union
import numpy as np
from qiskit.circuit.quantumcircuit import QuantumCircuit
from qiskit.circuit.library.generalized_gates import Diagonal
import qiskit.quantum_info as qi

def LRC(n: int, D: int, to_gate: bool = False, seed: Union[int, np.random.Generator] = None) -> QuantumCircuit:
    """
    Local Random Clifford

    Arguments
        n: qubit size
        D: depth
    Returns
        qc: quantum circuit
    """
    qc = QuantumCircuit(n)
    for l in range(1, D+1):
        if n & 1 and l & 1:
            for i in range((n - 1) // 2):
                qc.append(qi.random_unitary(4, seed = seed).to_instruction(), [2 * i, 2 * i + 1])
        if n & 1 and not l & 1:
            for i in range((n - 1) // 2):
                qc.append(qi.random_unitary(4, seed = seed).to_instruction(), [2 * i + 1, 2 * i + 2])
        if not n & 1 and l & 1:
            for i in range(n // 2):
                qc.append(qi.random_unitary(4, seed = seed).to_instruction(), [2 * i, 2 * i + 1])
        if not n & 1 and not l & 1:
            for i in range(n // 2 - 1):
                qc.append(qi.random_unitary(4, seed = seed).to_instruction(), [2 * i + 1, 2 * i + 2])
        qc.barrier()

    return qc.to_gate(label="LRC("+str(n)+","+str(D)+")") if to_gate else qc

def RDC(n: int, D: int, to_gate: bool = False, seed: Union[int, np.random.Generator] = None) -> QuantumCircuit:
    """
    Random Diagonal Clifford

    Arguments
        n: qubit size
        D: depth
    Returns
        qc: quantum circuit
    """
    if seed is not None:
        np.random.seed(seed)

    qc = QuantumCircuit(n)
    for l in range(D):
        thetas = np.random.uniform(low = 0, high = 2 * np.pi, size = 2 ** n)
        qc.append(Diagonal(np.exp(thetas * 1j)))
        qc.h(range(n))
    return qc.to_gate(label="RDC("+str(n)+","+str(D)+")") if to_gate else qc
