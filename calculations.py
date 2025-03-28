import numpy as np

# Predefined constants
g = 9.81  # Gravity (m/s^2)
Isp = 300  # Specific impulse (s)
rho_prop = 1000  # Density of propellant (kg/m^3)
rho_wall = 2700  # Density of wall material (kg/m^3)
rho_bulkhead = 2700  # Density of bulkhead material (kg/m^3)
d_prop = 1.0  # Propellant diameter (m)
d_total = 1.2  # Total diameter (m)
L_bulkhead = 0.5  # Bulkhead length (m)
m_payload = 500  # Assumed payload mass (kg)


# Functions for calculations
def delta_v(L1, L2, L3):
    v_exhaust = Isp * g

    # Mass calculations
    m_prop = [mass_propellant(d_prop, L, rho_prop) for L in [L1, L2, L3]]
    m_wall = [mass_wall(d_total, d_prop, L, rho_wall) for L in [L1, L2, L3]]
    m_bulkhead = mass_bulkhead(d_total, L_bulkhead, rho_bulkhead)

    # Stage mass ratios
    m_ratios = stage_mass_ratios(m_prop, m_wall, m_bulkhead)

    # Delta-v for each stage
    delta_v_stages = [v_exhaust * np.log(m0_mf) for m0_mf in m_ratios]

    # Total delta-v
    return sum(delta_v_stages)


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


print(delta_v(1, 1, 1))
