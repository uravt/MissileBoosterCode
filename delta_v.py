import constants
import numpy as np

# Functions

def mass_propellant(L_prop):
    return (np.pi * (constants.d_prop ** 2) / 4) * L_prop * constants.rho_prop

def mass_wall(L_wall):
    return (np.pi / 4) * ((constants.d_total ** 2) - (constants.d_prop ** 2)) * L_wall * constants.rho_wall
    
def delta_v(mass_ratio):
    return (constants.v_exhaust * np.log(mass_ratio))

def mass_ratio(lambda_value, epsilon_value):
    return ((epsilon_value + lambda_value) / (1 + lambda_value))

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
    epsilon_1 = (constants.m_bulkhead + m_wall1) / (m_prop1 + constants.m_bulkhead + m_wall1)
    epsilon_2 = (constants.m_bulkhead + m_wall2) / (m_prop2 + constants.m_bulkhead + m_wall2)
    epsilon_3 = (constants.m_bulkhead + m_wall3) / (m_prop3 + constants.m_bulkhead + m_wall3)

    # Compute Payload Ratios
    lambda_1 = (constants.m_payload + m_prop2 + m_prop3 + (2 * constants.m_bulkhead) + m_wall2 + m_wall3) / (m_prop1 + constants.m_bulkhead + m_wall1)
    lambda_2 = (constants.m_payload + m_prop3 + constants.m_bulkhead + m_wall3) / (m_prop2 + constants.m_bulkhead + m_wall2)
    lambda_3 = (constants.m_payload) / (m_prop3 + constants.m_bulkhead + m_wall3)

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
