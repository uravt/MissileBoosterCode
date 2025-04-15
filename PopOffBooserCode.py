import math
import sys
import subprocess
from selectors import SelectSelector

# Install numpy if not installed
try:
    import numpy as np
except ImportError:
    print("NumPy not found. Installing now...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])
    import numpy as np
    print("NumPy installed successfully!")

# Constants
g = 9.81  # Gravity (m/s^2)
Isp = 260  # Specific impulse (s)
rho_prop = 1960  # Density of propellant (kg/m^3)
rho_wall = 2700  # Density of wall material (kg/m^3)
rho_bulkhead = 2600  # Density of bulkhead material (kg/m^3)
d_prop = 0.5  # Propellant diameter (m)
d_total = 0.75  # Total diameter (m)
L_bulkhead = 0.5  # Bulkhead length (m)
m_payload = 250  # Assumed payload mass (kg)


def solve_quadratic(a, b, c):
    # Calculate the discriminant
    discriminant = math.sqrt(b ** 2 - 4 * a * c)
    # Calculate two solutions
    x1 = (-b + discriminant) / (2 * a)
    x2 = (-b - discriminant) / (2 * a)

    if ((x1 < L_total) and (x1 > 0)):
        return x1
    else:
        return x2
        
def compute_L1(burn_time, L_total):
    M = m_payload
    L = L_total
    
    R = math.exp((burn_time) / (2 * Isp)) # Mass Ratio Defined by Burn Time
    
    A = (np.pi / 4) * (d_prop) ** 2 * (rho_prop)
    B = (np.pi / 4) * (d_total ** 2) * (L_bulkhead) * (rho_bulkhead)
    C = (np.pi / 4) * ((d_prop) ** 2 - (rho_wall) ** 2) * (rho_wall)
    D = M + A + 2 * B + C
    E = M + A * L + 3 * B + C * L
    F = A * C + C ** 2
    G = A * B + 2 * B * C
    H = A * ((-1 * A) - C)
    I = D * A + E * ((-1 * A) - C)
    J = (C * E) + (A * B)
    K = F + H
    N = G + I
    O = B ** 2 + D * E
    P = K - (R * A)
    Q = N - (R * J)
    S = O - ((B * E) * R)

    L1 = solve_quadratic(P, Q, S)
    return L1



