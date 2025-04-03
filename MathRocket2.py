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

def get_float(prompt):
    while True:
        try:
            return float(input(prompt).strip())  # Strip removes extra spaces
        except ValueError:
            print("Invalid input! Please enter a numeric value.")

def mass_propellant(L_prop):
    return (np.pi * (d_prop ** 2) / 4) * L_prop * rho_prop

def mass_wall(L_wall):
    return (np.pi / 4) * ((d_total ** 2) - (d_prop ** 2)) * L_wall * rho_wall

message = """
Welcome to the Rocket Stage Optimization Program!
This program calculates the optimal Delta-V for a three-stage rocket,
ensuring the total stage length remains 6 meters.
Users will input individual stage lengths, and the program will compute
the resulting Delta-V based on mass properties and the rocket equation.
"""

print(message)

# Get stage lengths from user

L1 = get_float("Please enter stage length 1 (meters): ")
L2 = get_float("Please enter stage length 2 (meters): ")
L3 = get_float("Please enter stage length 3 (meters): ")

# Ensure total length constraint is met
if round(L1 + L2 + L3, 2) != 6:
  print("Error: The total stage length must be 5.5 meters.")

v_exhaust = Isp * g

# Compute mass for each stage
m_prop1 = mass_propellant(L1)
m_prop2 = mass_propellant(L2)
m_prop3 = mass_propellant(L3)

m_bulkhead = (np.pi / 4) * (d_total ** 2) * (L_bulkhead) * (rho_bulkhead)

m_wall1 = mass_wall(L1)
m_wall2 = mass_wall(L2)
m_wall3 = mass_wall(L3)


#mass_ratio1 = (m_payload + m_prop1 + m_prop2 + m_prop3 + (3 * m_bulkhead) + m_wall1 + m_wall2 + m_wall3) / (m_payload + m_prop1 + m_prop2 + (2 * m_bulkhead) + m_wall1 + m_wall2)
#mass_ratio2 = (m_payload + m_prop1 + m_prop2 + (2 * m_bulkhead) + m_wall1 + m_wall2) / (m_payload + m_prop1 + m_bulkhead + m_wall1)
#mass_ratio3 = (m_payload + m_prop1 + m_bulkhead + m_wall1) / (m_payload)

#mass_ratio1 = (m_payload + m_prop1 + m_prop2 + m_prop3) / (m_payload + m_prop1 + m_prop2)
#mass_ratio2 = (m_payload + m_prop1 + m_prop2) / (m_payload + m_prop1)
#mass_ratio3 = (m_payload + m_prop1) / (m_payload)

epsilon_1 = (m_bulkhead + m_wall1) / (m_prop1 + m_bulkhead + m_wall1)
epsilon_2 = (m_bulkhead + m_wall2) / (m_prop2 + m_bulkhead + m_wall2)
epsilon_3 = (m_bulkhead + m_wall3) / (m_prop3 + m_bulkhead + m_wall3)

lambda_1 = (m_payload + m_prop2 + m_prop3 + (2 * m_bulkhead) + m_wall2 + m_wall3) / (m_prop1 + m_bulkhead + m_wall1)
lambda_2 = (m_payload + m_prop3 + m_bulkhead + m_wall3) / (m_prop2 + m_bulkhead + m_wall2)
lambda_3 = (m_payload) / (m_prop3 + m_bulkhead + m_wall3)

mass_ratio1 = (1 + lambda_1) / (epsilon_1 + lambda_1)
mass_ratio2 = (1 + lambda_2) / (epsilon_2 + lambda_2)
mass_ratio3 = (1 + lambda_3) / (epsilon_3 + lambda_3)

delta_v1 = v_exhaust * np.log(mass_ratio1)
delta_v2 = v_exhaust * np.log(mass_ratio2)
delta_v3 = v_exhaust * np.log(mass_ratio3)

total_delta_v = delta_v1 + delta_v2 + delta_v3
print(total_delta_v)
