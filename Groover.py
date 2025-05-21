from qiskit import QuantumCircuit
from qiskit_aer.primitives import Sampler
import matplotlib.pyplot as plt
import numpy as np
import random
import time

def classical_search(target, items):
    for i, item in enumerate(items):
        if item == target:
            return i
    return -1

def oracle_operator(n_qubits, target_state):
    oracle = QuantumCircuit(n_qubits)
    for i, bit in enumerate(reversed(target_state)):
        if bit == '0':
            oracle.x(i)
    oracle.h(n_qubits - 1)
    oracle.mcx(list(range(n_qubits - 1)), n_qubits - 1)
    oracle.h(n_qubits - 1)
    for i, bit in enumerate(reversed(target_state)):
        if bit == '0':
            oracle.x(i)
    return oracle.to_gate(label="Oracle")

def diffusion_operator(n_qubits):
    diffuser = QuantumCircuit(n_qubits)
    diffuser.h(range(n_qubits))
    diffuser.x(range(n_qubits))
    diffuser.h(n_qubits - 1)
    diffuser.mcx(list(range(n_qubits - 1)), n_qubits - 1)
    diffuser.h(n_qubits - 1)
    diffuser.x(range(n_qubits))
    diffuser.h(range(n_qubits))
    return diffuser.to_gate(label="Diffusion")

def simulate_grover_vs_classical():
    qubit_range_simulate = range(3, 9)  # full simulation for 3-8 qubits
    qubit_range_total = range(3, 16)    # extend plot to 15 qubits

    classical_times = []
    grover_times = []
    grover_steps = []
    classical_steps = []

    for n_qubits in qubit_range_total:
        N = 2 ** n_qubits
        classical_steps.append(N)
        num_iterations = int(np.floor(np.pi / 4 * np.sqrt(N)))
        grover_steps.append(num_iterations)

        if n_qubits in qubit_range_simulate:
            print(f"\n--- Simulating {n_qubits} Qubits ---")
            items = [f"{i:0{n_qubits}b}" for i in range(N)]
            target = random.choice(items)

            # Classical
            start_classical = time.time()
            classical_search(target, items)
            end_classical = time.time()
            classical_times.append(end_classical - start_classical)

            # Grover's Algorithm Simulation
            grover = QuantumCircuit(n_qubits)
            grover.h(range(n_qubits))
            oracle = oracle_operator(n_qubits, target)
            diffuser = diffusion_operator(n_qubits)

            for _ in range(num_iterations):
                grover.append(oracle, range(n_qubits))
                grover.append(diffuser, range(n_qubits))

            grover.measure_all()
            start_quantum = time.time()
            sampler = Sampler()
            job = sampler.run(circuits=grover, shots=1024)
            result = job.result()
            end_quantum = time.time()
            grover_times.append(end_quantum - start_quantum)
        else:
            classical_times.append(None)
            grover_times.append(None)
            print(f"Skipped simulation for {n_qubits} qubits (too large)")

    # Plot theoretical step comparison
    plt.figure(figsize=(10, 6))
    plt.plot(classical_steps, classical_steps, 'r-', label='Classical Steps (N)')
    plt.plot(classical_steps, grover_steps, 'b-o', label="Grover Steps (~√N)")
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Database Size (N = 2^n)')
    plt.ylabel('Steps to Find Target')
    plt.title("Classical vs Grover's Algorithm Step Count (3 to 15 qubits)")
    plt.legend()
    plt.grid(True, which="both", linestyle="--", alpha=1)
    plt.tight_layout()
    plt.show()

simulate_grover_vs_classical()
