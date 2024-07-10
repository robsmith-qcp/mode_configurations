import os
import numpy as np
from mode_configurations.configurations import generate_geometric_configurations_zero_point

num_samples = 100

# H2 data sample from QChem output HF/STO-3G
atomic_symbols = np.array(["H", "H"])

# Equilibrium coordinates in Angstrom
R0 = np.array([[0.0000000000, 0.0000000000, 0.1478850754],
               [0.0000000000, 0.0000000000, 0.8601149246]])

# ν in cm^-1
frequency_cm1 = np.array([5481.25])

# μ in amu
reduced_masses_amu = np.array([1.0078])

# k in mDyn/Å and in N/m
forces_mdyn_per_ang = np.array([17.8401])
forces_n_per_m = forces_mdyn_per_ang * 100

# Normal modes in Angstroms
modes = np.array([[[-0.000, -0.000, 0.707],
                   [-0.000, -0.000, -0.707]]])

configurations, displacements = generate_geometric_configurations_zero_point(R0, modes, frequency_cm1, reduced_masses_amu, num_samples, forces_mdyn_per_ang)

# Generating an xyz output file to hold the configurations
initial_configuration = """
2
Configuration 0
H       0.0000000000     0.0000000000     0.1478850754
H       0.0000000000     0.0000000000     0.8601149246
"""
output_file = "h2_configurations.xyz"
n_atoms = R0.shape[0]
with open(output_file, "w") as f:
    f.write(initial_configuration.strip() + "\n")

    for i, config in enumerate(configurations):
        f.write(f"{n_atoms}\n")
        f.write(f"Configuration {i+1}\n")
        for atom, (x, y, z) in zip(atomic_symbols, config):
            f.write(f"{atom} {x:.6f} {y:.6f} {z:.6f}\n")

print(f"Generated multi-frame XYZ file: {output_file}")


