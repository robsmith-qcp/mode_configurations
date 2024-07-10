# tests/test_configurations.py

import numpy as np
import pytest
from mode_configurations.configurations import generate_geometric_configurations_zero_point

def test_generate_geometric_configurations_zero_point():
    # Known input values
    R0 = np.array([[0.0, 0.0, 0.0],
                   [1.0, 0.0, 0.0],
                   [0.0, 1.0, 0.0]])
    vibrational_modes = np.array([[[1.0, 0.0, 0.0],
                                   [0.0, 1.0, 0.0],
                                   [0.0, 0.0, 1.0]],
                                  [[0.0, 1.0, 0.0],
                                   [1.0, 0.0, 0.0],
                                   [0.0, 0.0, 1.0]]])
    frequencies = np.array([1000.0, 1500.0])  # in cm^-1
    reduced_masses = np.array([1.0, 1.5])  # in amu
    num_samples = 100
    forces = np.array([0.5, 0.75])  # in mDyn/Å
    seed = 42  # Set a random seed for reproducibility

    # Call the function
    configurations, displacements = generate_geometric_configurations_zero_point(
        R0, vibrational_modes, frequencies, reduced_masses, num_samples, seed)

    # Assertions
    assert configurations.shape == (num_samples, len(R0), 3)
    assert displacements.shape == (num_samples, len(R0), 3)

    # Check mean displacement is close to zero (zero-point motion should be centered around R0)
    assert np.allclose(np.mean(displacements, axis=0), 0, atol=1e-1)

    # Check standard deviation of displacements
    hbar = 1.054571817e-34
    c = 2.99792458e10
    amu_to_kg = 1.66053906660e-27
    angstrom_to_meter = 1e-10

    frequencies_rad_s = frequencies * c * 2 * np.pi
    reduced_masses_kg = reduced_masses * amu_to_kg
    sigma_expected = np.sqrt(hbar / (2 * reduced_masses_kg * frequencies_rad_s)) / angstrom_to_meter

    # Project displacements onto each mode
    mode_displacements = []
    for j in range(len(frequencies)):
        mode_flat = vibrational_modes[j].reshape(-1)
        projected_displacements = np.dot(displacements.reshape(num_samples, -1), mode_flat) / np.linalg.norm(mode_flat)
        mode_displacements.append(projected_displacements)

    mode_displacements = np.array(mode_displacements).T

    for i in range(len(frequencies)):
        mode_displacement_std = np.std(mode_displacements[:, i])
        assert np.allclose(mode_displacement_std, sigma_expected[i], atol=1e-1)

if __name__ == "__main__":
    pytest.main()

