try:
    import scipy
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "scipy"])
    import scipy
import numpy as np
from scipy.optimize import least_squares

# Constants
density_pipe = 1960  # kg/m^3
density_base = 2600  # kg/m^3
d_inner = 0.5        # m
d_outer = 0.75       # m
L_total = 6          # total length constraint
target_Mr1 = np.exp(1/52)  # from 10-second burn setup
M_b = (np.pi / 4) * d_outer**2 * 0.5 * density_base

# Define system of equations
def system(vars, L1_fixed):
    L2, L3 = vars
    Mp1 = np.pi * (d_inner**2) / 4 * L1_fixed * density_pipe
    Mp2 = np.pi * (d_inner**2) / 4 * L2 * density_pipe
    Mp3 = np.pi * (d_inner**2) / 4 * L3 * density_pipe
    Mw1 = (np.pi / 4) * (d_outer**2 - d_inner**2) * L1_fixed * density_pipe
    Mw2 = (np.pi / 4) * (d_outer**2 - d_inner**2) * L2 * density_pipe
    Mw3 = (np.pi / 4) * (d_outer**2 - d_inner**2) * L3 * density_pipe
    epsilon = (M_b + Mw1) / (Mp1 + M_b + Mw1)
    lambda_ = (250 + Mp2 + Mp3 + 2*M_b + Mw2 + Mw3) / (Mp1 + M_b + Mw1)
    Mr1 = (1 + lambda_) / (epsilon + lambda_)
    eq1 = L1_fixed + L2 + L3 - L_total
    eq2 = Mr1 - target_Mr1
    return [eq1, eq2]

# --- Main program ---
while True:
    # Manually input L1
    L1_input = float(input("\nEnter L1 (in meters): "))

    # Smart initial guess: L1 = L2 = L3 initially
    initial_guess_value = L_total / 3  # 6/3 = 2 meters
    initial_guess = [initial_guess_value, initial_guess_value]

    # Solve using least squares
    result = least_squares(system, initial_guess, args=(L1_input,))
    L2_solution, L3_solution = result.x

    # Output
    print("\nSolution:")
    print(f"L1 = {L1_input:.4f} m")
    print(f"L2 = {L2_solution:.4f} m")
    print(f"L3 = {L3_solution:.4f} m")

    # Check if solution is physical
    if L2_solution < 0 or L3_solution < 0:
        print("\n⚠️ Warning: Solution has negative length(s). Please enter a new L1.")
    else:
        print("\n✅ Solution is physical and acceptable.")
        break  # Exit loop if solution is good

