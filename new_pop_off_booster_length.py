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
    F = E * (1 - R)

    L1 = F / C

    return L1

# Important Note - This function accounts for the length of the bulkheads so 
# it is important that the main code does not call this function using anything other than the total missile length
