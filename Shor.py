import matplotlib.pyplot as plt
import numpy as np

# Number of bits for the integers we try to factor
bit_sizes = np.arange(2, 50, 2)  # from 2 to 48 bits

# Classical factoring time model (exponential)
# For demonstration: classical_time = 2^(bit_size/2)
classical_time = 2**(bit_sizes / 2)

# Shor's algorithm time model (polynomial)
# For demonstration: shor_time = bit_size^3
shor_time = bit_sizes**3

plt.figure(figsize=(10, 6))
plt.plot(bit_sizes, classical_time, label="Classical factoring (exp)")
plt.plot(bit_sizes, shor_time, label="Shor's algorithm (poly)")
plt.yscale('log')  # log scale to show difference clearly

plt.xlabel("Number size (bits)")
plt.ylabel("Time (arbitrary units, log scale)")
plt.title("Theoretical Time Complexity: Classical vs Shor's Algorithm")
plt.legend()
plt.grid(True, which="both", ls="--")
plt.show()