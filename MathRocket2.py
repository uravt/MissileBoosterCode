import sys
import subprocess

# Install numpy if not installed
try:
    import numpy as np
except ImportError:
    print("NumPy not found. Installing now...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])
    import numpy as np
    print("NumPy installed successfully!")


# Predefined constants
g = 9.81  # Gravity (m/s^2)
Isp = 260  # Specific impulse (s)
rho_prop = 1960  # Density of propellant (kg/m^3)
rho_wall = 2700  # Density of wall material (kg/m^3)
rho_bulkhead = 2700  # Density of bulkhead material (kg/m^3)
d_prop = 0.6  # Propellant diameter (m)
d_total = 0.75  # Total diameter (m)
L_bulkhead = 0.5  # Bulkhead length (m)
m_payload = 250  # Assumed payload mass (kg)


def mass_propellant(d_prop, L, rho_prop):
    return (np.pi * (d_prop ** 2) / 4) * L * rho_prop


def mass_wall(d_total, d_prop, L, rho_wall):
    return (np.pi / 4) * ((d_total ** 2) - (d_prop ** 2)) * L * rho_wall


def mass_bulkhead(d_total, L, rho_bulkhead):
    return (np.pi / 4) * (d_total ** 2) * L * rho_bulkhead


def stage_mass_ratios(m_prop, m_wall, m_bulkhead):
    m0_1 = m_payload + sum(m_prop) + 3 * m_bulkhead + sum(m_wall)
    mf_1 = m_payload + sum(m_prop[:2]) + 2 * m_bulkhead + sum(m_wall[:2])

    m0_2 = mf_1
    mf_2 = m_payload + m_prop[0] + m_bulkhead + m_wall[0]

    m0_3 = mf_2
    mf_3 = m_payload

    return (m0_1 / mf_1, m0_2 / mf_2, m0_3 / mf_3)


# Functions for calculations
def delta_v():
    # Function to safely get a float input
    def get_float(prompt):
        while True:
            try:
                return float(input(prompt).strip())  # Strip removes extra spaces
            except ValueError:
                print("Invalid input! Please enter a numeric value.")

    message = """
    Welcome to the Rocket Stage Optimization Program!
    This program calculates the optimal Delta-V for a three-stage rocket,
    ensuring the total stage length remains 5.5 meters.
    Users will input individual stage lengths, and the program will compute 
    the resulting Delta-V based on mass properties and the rocket equation.
    """

    print(message)

    # Get stage lengths from user
    L1 = get_float("Please enter stage length 1 (meters): ")
    L2 = get_float("Please enter stage length 2 (meters): ")
    L3 = get_float("Please enter stage length 3 (meters): ")

    # Ensure total length constraint is met
    if round(L1 + L2 + L3, 2) != 5.5:
        print("Error: The total stage length must be 5.5 meters.")
        return None

    v_exhaust = Isp * g

    # Compute mass for each stage
    m_prop = [mass_propellant(d_prop, L, rho_prop) for L in [L1, L2, L3]]
    m_wall = [mass_wall(d_total, d_prop, L, rho_wall) for L in [L1, L2, L3]]
    m_bulkhead = mass_bulkhead(d_total, L_bulkhead, rho_bulkhead)

    # Compute stage mass ratios correctly
    m_ratios = stage_mass_ratios(m_prop, m_wall, m_bulkhead)

    # Compute delta-v per stage
    delta_v_stages= [v_exhaust * np.log(m0_mf) for m0_mf in m_ratios]
    # Total delta-v
    total_dv = sum(delta_v_stages)
    print(f"Optimized Delta-V: {total_dv:.2f} m/s")
    return total_dv
delta_v()