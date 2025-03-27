{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "94c3a08e-491d-4f06-af4e-432c14fd4a4b",
   "metadata": {},
   "outputs": [
    {
     "name": "stdin",
     "output_type": "stream",
     "text": [
      "Please enter stage length 1 (meters):  1\n",
      "Please enter stage length 2 (meters):  1.5\n",
      "Please enter stage length 3 (meters):  3\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Optimized Delta-V: 8657.69 m/s\n"
     ]
    },
    {
     "data": {
      "text/plain": [
       "8657.690324397363"
      ]
     },
     "execution_count": 9,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "import numpy as np\n",
    "# Predefined constants\n",
    "g = 9.81  # Gravity (m/s^2)\n",
    "Isp = 260  # Specific impulse (s)\n",
    "rho_prop = 1960  # Density of propellant (kg/m^3)\n",
    "rho_wall = 2700  # Density of wall material (kg/m^3)\n",
    "rho_bulkhead = 2700  # Density of bulkhead material (kg/m^3)\n",
    "d_prop = 0.6  # Propellant diameter (m)\n",
    "d_total = 0.75  # Total diameter (m)\n",
    "L_bulkhead = 0.5  # Bulkhead length (m)\n",
    "m_payload = 250  # Assumed payload mass (kg)\n",
    "def mass_propellant(d_prop, L, rho_prop):\n",
    "    return (np.pi * (d_prop**2) / 4) * L * rho_prop\n",
    "\n",
    "def mass_wall(d_total, d_prop, L, rho_wall):\n",
    "    return (np.pi / 4) * ((d_total**2) - (d_prop**2)) * L * rho_wall\n",
    "\n",
    "def mass_bulkhead(d_total, L, rho_bulkhead):\n",
    "    return (np.pi / 4) * (d_total**2) * L * rho_bulkhead\n",
    "\n",
    "def stage_mass_ratios(m_prop, m_wall, m_bulkhead):\n",
    "    m0_1 = m_payload + sum(m_prop) + 3 * m_bulkhead + sum(m_wall)\n",
    "    mf_1 = m_payload + sum(m_prop[:2]) + 2 * m_bulkhead + sum(m_wall[:2])\n",
    "    \n",
    "    m0_2 = mf_1\n",
    "    mf_2 = m_payload + m_prop[0] + m_bulkhead + m_wall[0]\n",
    "    \n",
    "    m0_3 = mf_2\n",
    "    mf_3 = m_payload\n",
    "    \n",
    "    return (m0_1 / mf_1, m0_2 / mf_2, m0_3 / mf_3)\n",
    "    \n",
    "# Functions for calculations\n",
    "def delta_v(): \n",
    "    # Function to safely get a float input\n",
    "    def get_float(prompt):\n",
    "        while True:\n",
    "            try:\n",
    "                return float(input(prompt).strip())  # Strip removes extra spaces\n",
    "            except ValueError:\n",
    "                print(\"Invalid input! Please enter a numeric value.\")\n",
    "\n",
    "    # Get stage lengths from user\n",
    "    L1 = get_float(\"Please enter stage length 1 (meters): \")\n",
    "    L2 = get_float(\"Please enter stage length 2 (meters): \")\n",
    "    L3 = get_float(\"Please enter stage length 3 (meters): \")\n",
    "\n",
    "    # Ensure total length constraint is met\n",
    "    if round(L1 + L2 + L3, 2) != 5.5:\n",
    "        print(\"Error: The total stage length must be 5.5 meters.\")\n",
    "        return None\n",
    "\n",
    "    v_exhaust = Isp * g\n",
    "    \n",
    "    # Compute mass for each stage\n",
    "    m_prop = [mass_propellant(d_prop, L, rho_prop) for L in [L1, L2, L3]]\n",
    "    m_wall = [mass_wall(d_total, d_prop, L, rho_wall) for L in [L1, L2, L3]]\n",
    "    m_bulkhead = mass_bulkhead(d_total, L_bulkhead, rho_bulkhead)\n",
    "\n",
    "    # Compute stage mass ratios correctly\n",
    "    m_ratios = stage_mass_ratios(m_prop, m_wall, m_bulkhead)\n",
    "\n",
    "    # Compute delta-v per stage\n",
    "    delta_v_stages = [v_exhaust * np.log(m0_mf) for m0_mf in m_ratios]\n",
    "\n",
    "    # Total delta-v\n",
    "    total_dv = sum(delta_v_stages)\n",
    "    print(f\"Optimized Delta-V: {total_dv:.2f} m/s\")\n",
    "    return total_dv\n",
    "\n",
    "# Run the function\n",
    "delta_v()\n",
    "\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "01e4e8cf-fc45-42d7-b166-ad1735bd68c2",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
