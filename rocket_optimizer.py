import random
import matplotlib.pyplot as plt
import numpy as np
from prettytable import PrettyTable

# Constants
g = 9.81  # Gravity (m/s^2)
Isp = 260  # Specific impulse (s)
rho_prop = 1960  # Density of propellant (kg/m^3)
rho_wall = 2700  # Density of wall material (kg/m^3)
rho_bulkhead = 2600  # Density of bulkhead material (kg/m^3)
d_prop = 0.5  # Propellant diameter (m)
d_total = 0.75  # Total diameter (m)
L_bulkhead = 0.5  # Bulkhead length (m)
m_payload = 250  # Payload mass (kg)

def get_float(prompt):
    while True:
        try:
            return float(input(prompt).strip())  # Strip removes extra spaces
        except ValueError:
            print("Invalid input! Please enter a numeric value.")

rocket_length = 0

# Helper functions
def mass_propellant(L_prop):
    return (np.pi * (d_prop ** 2) / 4) * L_prop * rho_prop

def mass_wall(L_wall):
    return (np.pi / 4) * ((d_total ** 2) - (d_prop ** 2)) * L_wall * rho_wall

# Fitness function for the genetic algorithm
def fitness_function(ind, rocket_length):
    L1, L2, L3 = ind

    # Constraint: sum of individual lengths must equal total length 
    if L1 <= 0 or L2 <= 0 or L3 <= 0 or not np.isclose(L1 + L2 + L3, rocket_length, atol=0.01):
        return -1e6  # Penalize invalid solutions

    v_exhaust = Isp * g

    # Compute masses
    m_prop1 = mass_propellant(L1)
    m_prop2 = mass_propellant(L2)
    m_prop3 = mass_propellant(L3)

    m_wall1 = mass_wall(L1)
    m_wall2 = mass_wall(L2)
    m_wall3 = mass_wall(L3)

    m_bulkhead = (np.pi / 4) * (d_total ** 2) * L_bulkhead * rho_bulkhead

    # Mass ratios and efficiencies
    epsilon_1 = (m_bulkhead + m_wall1) / (m_prop1 + m_bulkhead + m_wall1)
    epsilon_2 = (m_bulkhead + m_wall2) / (m_prop2 + m_bulkhead + m_wall2)
    epsilon_3 = (m_bulkhead + m_wall3) / (m_prop3 + m_bulkhead + m_wall3)

    lambda_1 = (m_payload + m_prop2 + m_prop3 + 2 * m_bulkhead + m_wall2 + m_wall3) / (m_prop1 + m_bulkhead + m_wall1)
    lambda_2 = (m_payload + m_prop3 + m_bulkhead + m_wall3) / (m_prop2 + m_bulkhead + m_wall2)
    lambda_3 = m_payload / (m_prop3 + m_bulkhead + m_wall3)

    mass_ratio1 = (1 + lambda_1) / (epsilon_1 + lambda_1)
    mass_ratio2 = (1 + lambda_2) / (epsilon_2 + lambda_2)
    mass_ratio3 = (1 + lambda_3) / (epsilon_3 + lambda_3)

    try:
        delta_v1 = v_exhaust * np.log(mass_ratio1)
        delta_v2 = v_exhaust * np.log(mass_ratio2)
        delta_v3 = v_exhaust * np.log(mass_ratio3)
    except ValueError:
        return -1e6  # Penalize if log gets invalid due to mass ratio ≤ 0

    total_delta_v = delta_v1 + delta_v2 + delta_v3
    return total_delta_v  # Maximize this

# Create the initial population
def create_initial_population(size, total_length):
    population = []
    for _ in range(size):
        r = sorted([random.random(), random.random()])
        L1 = r[0] * total_length
        L2 = (r[1] - r[0]) * total_length
        L3 = (1 - r[1]) * total_length
        population.append([L1, L2, L3])
    return population


# Selection function using tournament selection
def selection(population, fitnesses, tournament_size=3):
    selected = []
    for _ in range(len(population)):
        tournament = random.sample(list(zip(population, fitnesses)), tournament_size)
        winner = max(tournament, key=lambda x: x[1])[0]
        selected.append(winner)
    return selected


# Crossover function
def crossover(parent1, parent2, rocket_length):
    alpha = random.random()
    child1 = [alpha * p1 + (1 - alpha) * p2 for p1, p2 in zip(parent1, parent2)]
    child2 = [(1 - alpha) * p1 + alpha * p2 for p1, p2 in zip(parent1, parent2)]

    # Normalize to maintain total length
    def normalize(child):
        total = sum(child)
        return [L * rocket_length / total for L in child]

    return normalize(child1), normalize(child2)


# Mutation function
def mutation(individual, mutation_rate, lower_bound, upper_bound, rocket_length):
    individual = list(individual)
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            delta = random.uniform(-0.5, 0.5)
            individual[i] += delta
            individual[i] = max(lower_bound, min(upper_bound, individual[i]))

    # Normalize again to maintain sum = rocket_length
    total = sum(individual)
    individual = [L * rocket_length / total for L in individual]
    return individual



# Genetic Algorithm function
def genetic_algorithm(population_size, lower_bound, upper_bound, generations, mutation_rate, rocket_length):
    population = create_initial_population(population_size, rocket_length)

    # Prepare for plotting
    fig, axs = plt.subplots(3, 1, figsize=(12, 18))
    best_performers = []
    all_populations = []

    # Prepare for table
    table = PrettyTable()
    table.field_names = ["Generation", "Length 1", "Length 2", "Length 3", "Fitness"]

    for generation in range(generations):
        fitnesses = [fitness_function(ind, rocket_length) for ind in population]

        # Store the best performer of the current generation
        best_individual = max(population, key=lambda ind: fitness_function(ind, rocket_length))
        best_fitness = fitness_function(best_individual, rocket_length)
        best_performers.append((best_individual, best_fitness))
        all_populations.append(population[:])
        table.add_row([generation, best_individual[0], best_individual[1], best_individual[2], best_fitness])

        population = selection(population, fitnesses)

        new_population = []
        for i in range(0, len(population), 2):
            parent1 = population[i]
            parent2 = population[i + 1]
            child1, child2 = crossover(parent1, parent2, rocket_length)
            new_population.append(mutation(child1, mutation_rate, lower_bound, upper_bound, rocket_length))
            new_population.append(mutation(child2, mutation_rate, lower_bound, upper_bound, rocket_length))

        new_population[0] = best_individual
        population = new_population

    # Print the table
    print(table)

    # Plotting population stats
    final_population = all_populations[-1]
    final_fitnesses = [fitness_function(ind, rocket_length) for ind in final_population]

    axs[0].scatter(range(len(final_population)), [ind[0] for ind in final_population], color='blue', label='L1')
    axs[0].scatter([final_population.index(best_individual)], [best_individual[0]], color='cyan', s=100,
                   label='Best L1')
    axs[0].set_ylabel('L1', color='blue')
    axs[0].legend(loc='upper left')

    axs[1].scatter(range(len(final_population)), [ind[1] for ind in final_population], color='green', label='L2')
    axs[1].scatter([final_population.index(best_individual)], [best_individual[1]], color='magenta', s=100,
                   label='Best L2')
    axs[1].set_ylabel('L2', color='green')
    axs[1].legend(loc='upper left')

    axs[2].scatter(range(len(final_population)), [ind[2] for ind in final_population], color='red', label='L3')
    axs[2].scatter([final_population.index(best_individual)], [best_individual[2]], color='yellow', s=100,
                   label='Best L3')
    axs[2].set_ylabel('L3', color='red')
    axs[2].set_xlabel('Individual Index')
    axs[2].legend(loc='upper left')

    axs[0].set_title(f'Final Generation ({generations}) Population Solutions')

    # Plot L1, L2, L3 over generations
    generations_list = range(1, len(best_performers) + 1)
    a_values = [ind[0][0] for ind in best_performers]
    b_values = [ind[0][1] for ind in best_performers]
    c_values = [ind[0][2] for ind in best_performers]
    fig, ax = plt.subplots()
    ax.plot(generations_list, a_values, label='L1', color='blue')
    ax.plot(generations_list, b_values, label='L2', color='green')
    ax.plot(generations_list, c_values, label='L3', color='red')
    ax.set_xlabel('Generation')
    ax.set_ylabel('Lengths')
    ax.set_title('Lengths Over Generations')
    ax.legend()

    # Plot delta-V over generations
    best_fitness_values = [fit[1] for fit in best_performers]
    min_fitness_values = [min([fitness_function(ind, rocket_length) for ind in population]) for population in all_populations]
    max_fitness_values = [max([fitness_function(ind, rocket_length) for ind in population]) for population in all_populations]
    fig, ax = plt.subplots()
    ax.plot(generations_list, best_fitness_values, label='Best Fitness', color='black')
    ax.fill_between(generations_list, min_fitness_values, max_fitness_values, color='gray', alpha=0.5,
                    label='Fitness Range')
    ax.set_xlabel('Generation')
    ax.set_ylabel('Delta V')
    ax.set_title('Delta V Over Generations')
    ax.legend()

    plt.show()

    return max(population, key=lambda ind: fitness_function(ind, rocket_length))
