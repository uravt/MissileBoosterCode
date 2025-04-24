import math
import numpy as np
import constants

def solve_quadratic(a, b, c, contraint):
    # Calculate the discriminant
    discriminant = math.sqrt((b ** 2) - 4 * a * c)
    # Calculate two solutions
    x1 = (-b + discriminant) / (2 * a)
    x2 = (-b - discriminant) / (2 * a)

    if ((x1 < contraint) and (x1 > 0)):
        return x1
    else:
        return x2
        
def compute_L1(burn_time, length):
    M = constants.m_payload
    L = length
    
    R = math.exp((burn_time) / (2 * constants.Isp)) # Mass Ratio Defined by Burn Time
    
    A = (np.pi / 4) * ((constants.d_total**2) - (constants.d_prop**2)) * constants.rho_wall
    B = (np.pi / 4) * (constants.d_total ** 2) * (constants.L_bulkhead) * (constants.rho_bulkhead)
    C = (np.pi / 4) * (constants.d_prop**2) * constants.rho_wall
    D = M + (C * L) + (A * L) + (3 * B)
    E = M + (C * L) + (A * L) + (2 * B)
    F = A + C
    G = (B ** 2) + (D * E)
    H = (A * B) + (B * F) - (C * E) - (D * F)
    I = (A * F) + (C * F)
    J = (B * D)
    K = (A * D) - (B * C)
    N = (A * C)
    O = (I + (R * N))
    Q = H - (K * R)
    S = (G - (R * J))

    L1 = solve_quadratic(O, Q, S, length)
    return L1
