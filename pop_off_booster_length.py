import math
import numpy as np
import constants

def solve_quadratic(a, b, c, contraint):
    # Calculate the discriminant
    discriminant = math.sqrt(b ** 2 - 4 * a * c)
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
    
    A = (np.pi / 4) * (constants.d_prop) ** 2 * (constants.rho_prop)
    B = (np.pi / 4) * (constants.d_total ** 2) * (constants.L_bulkhead) * (constants.rho_bulkhead)
    C = (np.pi / 4) * ((constants.d_total)**2 - (constants.d_prop**2)) * constants.rho_wall
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

    L1 = solve_quadratic(P, Q, S, length)
    return L1