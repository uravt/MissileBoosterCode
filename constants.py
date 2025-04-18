import numpy as np

# Constants for the rocket design problem

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