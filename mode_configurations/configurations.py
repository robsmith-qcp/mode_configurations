import numpy as np
from scipy.stats import norm

def generate_geometric_configurations_zero_point(R0, vibrational_modes, frequencies, reduced_masses, num_samples, seed=None):
    """
    Generate normally distributed geometric configurations accounting for zero-point motion.
    
    Parameters:
    R0: array-like, shape (n_atoms, 3)
        Equilibrium coordinates of the molecule in Angstrom.
    vibrational_modes: array-like, shape (n_modes, n_atoms, 3)
        Normalized vibrational mode vectors in Angstroms.
    frequencies: array-like, shape (n_modes,)
        Frequencies of the normal modes (in cm^-1).
    reduced_masses: array-like, shape (n_modes,)
        Reduced masses associated with the normal modes (in amu).
    num_samples: int
        Number of geometric configurations to generate.
    seed: int, optional
        Random seed for reproducibility.
    
    Returns:
    configurations: array, shape (num_samples, n_atoms, 3)
        Generated geometric configurations.
    displacements: array, shape (num_samples, n_atoms, 3)
        Displacements from the equilibrium positions.
    """

    # Set random seed for reproducibility
    if seed is not None:
        np.random.seed(seed)

    # Constants
    hbar = 1.054571817e-34  # Reduced Planck's constant in J·s
    c = 2.99792458e10  # Speed of light in cm/s
    amu_to_kg = 1.66053906660e-27  # Conversion factor from amu to kg
    angstrom_to_meter = 1e-10  # Conversion factor from Angstrom to meter
    n_modes = len(frequencies)

    # Convert frequencies from cm^-1 to rad/s
    frequencies_rad_s = frequencies * c * 2 * np.pi  # Convert to rad/s
    print("Frequencies in rad/s:", frequencies_rad_s)
    
    # Convert reduced masses from amu to kg
    reduced_masses_kg = reduced_masses * amu_to_kg
    print("Reduced masses in kg:", reduced_masses_kg)
    
    # Calculate standard deviations for zero-point motion displacements
    sigma = np.sqrt(hbar / (2 * reduced_masses_kg * frequencies_rad_s)) / angstrom_to_meter  # In Angstroms
    print("Standard deviation (sigma) in Angstroms:", sigma)

    # Generate deterministic normally distributed values
    #quantiles = np.linspace(0, 1, num_samples + 2)[1:-1]  # Avoiding exact 0 and 1
    #delta = norm.ppf(quantiles).reshape(-1, 1) * sigma

    # Generate random values in a Gaussian distribution
    delta = np.random.normal(0, sigma, (num_samples, n_modes))

    # Generate configurations
    displacements = np.zeros((num_samples, len(R0), 3))
    configurations = np.zeros((num_samples, len(R0), 3))
    for i in range(num_samples):
        displacement = np.zeros((len(R0), 3))
        for j in range(n_modes):
            mode_displacement = delta[i, j] * vibrational_modes[j]  # Mode displacements in Angstroms
            displacement += mode_displacement
            #print("Displacement: ", displacement)
        displacements[i] = displacement
        configurations[i] = R0 + displacement

    return configurations, displacements
