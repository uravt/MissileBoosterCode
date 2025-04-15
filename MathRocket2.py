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
rho_bulkhead = 2600  # Density of bulkhead material (kg/m^3)
d_prop = 0.5  # Propellant diameter (m)
d_total = 0.75  # Total diameter (m)
L_bulkhead = 0.5  # Bulkhead length (m)
m_payload = 250  # Assumed payload mass (kg)
v_exhaust = Isp * g # exhaust velocity (m/s)
m_bulkhead = (np.pi / 4) * (d_total ** 2) * (L_bulkhead) * (rho_bulkhead) # mass of bulkhead (kg)

# Functions

def mass_propellant(L_prop):
    return (np.pi * (d_prop ** 2) / 4) * L_prop * rho_prop

def mass_wall(L_wall):
    return (np.pi / 4) * ((d_total ** 2) - (d_prop ** 2)) * L_wall * rho_wall
    
def delta_v(mass_ratio):
    delta_v =  v_exhaust * np.log(mass_ratio)
    return delta_v

def mass_ratio(lambda_value, epsilon_value):
    mass_ratio = (1 + lambda_value) / (epsilon_value + lambda_value)

def total_delta_v(L1, L2, L3):
    
    # Compute propellant mass for each stage
    m_prop1 = mass_propellant(L1)
    m_prop2 = mass_propellant(L2)
    m_prop3 = mass_propellant(L3)

    # Compute wall mass for each stage
    m_wall1 = mass_wall(L1)
    m_wall2 = mass_wall(L2)
    m_wall3 = mass_wall(L3)

    # Compute Structural Coefficients 
    epsilon_1 = (m_bulkhead + m_wall1) / (m_prop1 + m_bulkhead + m_wall1)
    epsilon_2 = (m_bulkhead + m_wall2) / (m_prop2 + m_bulkhead + m_wall2)
    epsilon_3 = (m_bulkhead + m_wall3) / (m_prop3 + m_bulkhead + m_wall3)

    # Compute Payload Ratios
    lambda_1 = (m_payload + m_prop2 + m_prop3 + (2 * m_bulkhead) + m_wall2 + m_wall3) / (m_prop1 + m_bulkhead + m_wall1)
    lambda_2 = (m_payload + m_prop3 + m_bulkhead + m_wall3) / (m_prop2 + m_bulkhead + m_wall2)
    lambda_3 = (m_payload) / (m_prop3 + m_bulkhead + m_wall3)

    # Compute Mass Ratios
    mass_ratio1 = mass_ratio(lambda_1, epsilon_1)
    mass_ratio2 = mass_ratio(lambda_2, epsilon_2)
    mass_ratio3 = mass_ratio(lambda_3, epsilon_3)

    # Compute Stage Delta_V Values
    delta_v1 = delta_v(mass_ratio1)
    delta_v2 = delta_v(mass_ratio2)
    delta_v3 = delta_v(mass_ratio3)

    # Compute Total Delta_V for the Rocket and return the value
    return delta_v1 + delta_v2 + delta_v3
 
