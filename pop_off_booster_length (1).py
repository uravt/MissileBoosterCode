import math
import numpy as np
import constants

def compute_L1(burn_time, length_total):
    M = constants.m_payload
    L_r = length_total - (3 * constants.L_bulkhead) # Reduced length
    
    R = math.exp((burn_time) / (2 * constants.Isp)) # Mass Ratio Defined by Burn Time
    
    A = (np.pi / 4) * ((constants.d_total**2) - (constants.d_prop**2)) * constants.rho_wall
    B = (np.pi / 4) * (constants.d_total ** 2) * (constants.L_bulkhead) * (constants.rho_bulkhead)
    C = (np.pi / 4) * (constants.d_prop**2) * constants.rho_prop
    D = A + C
    E = M + (3 * B) + (D * L_r)
    F = E * (R - 1)
    G = C * R

    L1 = F / G

    return L1
