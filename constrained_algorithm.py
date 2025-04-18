import random
import matplotlib.pyplot as plt
import numpy as np
from prettytable import PrettyTable
import delta_v

rocket_length = 10 # Placeholder for rocket length


# Fitness function for the genetic algorithm
def fitness_function_fixed_L1(ind, L1, rocket_length):
    L2, L3 = ind

    # Constraint: sum of individual lengths must equal total length 
    if L2 <= 0 or L3 <= 0 or not np.isclose(L1 + L2 + L3, rocket_length, atol=0.01):
        return -1e6 # Penalize invalid solutions
    
    return delta_v.total_delta_v(L1, L2, L3) # Maximize this


# Create the initial population
def create_initial_population_fixed_L1(size, remaining_length):
    population = []
    for _ in range(size):
        r = random.random()
        L2 = r * remaining_length
        L3 = remaining_length - L2
        population.append([L2, L3])
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
def crossover_fixed_L1(parent1, parent2, remaining_length):
    alpha = random.random()
    child1 = [alpha * p1 + (1 - alpha) * p2 for p1, p2 in zip(parent1, parent2)]
    child2 = [(1 - alpha) * p1 + alpha * p2 for p1, p2 in zip(parent1, parent2)]

    # Normalize to maintain total length
    def normalize(child):
        total = sum(child)
        return [L * remaining_length / total for L in child]

    return normalize(child1), normalize(child2)

def mutation_fixed_L1(individual, mutation_rate, lower_bound, upper_bound, remaining_length):
    individual = list(individual)
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            delta = random.uniform(-0.5, 0.5)
            individual[i] += delta
            individual[i] = max(lower_bound, min(upper_bound, individual[i]))
    total = sum(individual)
    return [L * remaining_length / total for L in individual]

def genetic_algorithm_fixed_L1(population_size, lower_bound, upper_bound, generations, mutation_rate, rocket_length, burn_time):
    L1 = compute_L1(burn_time=burn_time, length=rocket_length)
    remaining_length = rocket_length - L1

    population = create_initial_population_fixed_L1(population_size, remaining_length)

    best_performers = []
    all_populations = []

    for generation in range(generations):
        fitnesses = [fitness_function_fixed_L1(ind, L1, rocket_length) for ind in population]
        best_individual = max(population, key=lambda ind: fitness_function_fixed_L1(ind, L1, rocket_length))
        best_fitness = fitness_function_fixed_L1(best_individual, L1, rocket_length)
        best_performers.append(((L1, *best_individual), best_fitness))
        all_populations.append(population[:])

        population = selection(population, fitnesses)

        new_population = []
        for i in range(0, len(population), 2):
            parent1 = population[i]
            parent2 = population[(i + 1) % len(population)]
            child1, child2 = crossover_fixed_L1(parent1, parent2, remaining_length)
            new_population.append(mutation_fixed_L1(child1, mutation_rate, lower_bound, upper_bound, remaining_length))
            new_population.append(mutation_fixed_L1(child2, mutation_rate, lower_bound, upper_bound, remaining_length))

        new_population[0] = best_individual
        population = new_population

    best_final = max(population, key=lambda ind: fitness_function_fixed_L1(ind, L1, rocket_length))
    best_solution = (L1, *best_final)
    return best_solution, best_performers