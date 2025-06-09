import random
import matplotlib.pyplot as plt
import numpy as np
from prettytable import PrettyTable
import delta_v
import new_pop_off_booster_length

rocket_length = 10 # Placeholder for rocket length
L1 = new_pop_off_booster_length.compute_L1(burn_time=10, length_total=rocket_length)

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

def genetic_algorithm_fixed_L1(population_size, lower_bound, upper_bound, generations, mutation_rate, rocket_length):
    
    #L1 and remaining length calculation
    L1 = new_pop_off_booster_length.compute_L1(burn_time=10, length_total=rocket_length)
    remaining_length = rocket_length - L1

    population = create_initial_population_fixed_L1(population_size, remaining_length)

    # Prepare for plotting
    fig, axs = plt.subplots(3, 1, figsize=(12, 18))
    best_performers = []
    all_populations = []

    # Prepare for table
    table = PrettyTable()
    table.field_names = ["Generation", "Length 1", "Length 2", "Length 3", "Fitness"]

    for generation in range(generations):
        fitnesses = [fitness_function_fixed_L1(ind, L1, rocket_length) for ind in population]

        # Store the best performer of the current generation
        best_individual = max(population, key=lambda ind: fitness_function_fixed_L1(ind, L1, rocket_length))
        best_fitness = fitness_function_fixed_L1(best_individual, L1, rocket_length)
        best_performers.append(((L1, *best_individual), best_fitness))
        all_populations.append(population[:])
        table.add_row([generation, L1, best_individual[0], best_individual[1], best_fitness])

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

    # Plotting population stats
    final_population = all_populations[-1]
    final_fitnesses = [fitness_function_fixed_L1(ind, L1, rocket_length) for ind in final_population]

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

    axs[2].scatter(range(len(final_population)), [rocket_length - L1 - ind[0] for ind in final_population], color='red', label='L3')
    axs[2].scatter([final_population.index(best_individual)], [rocket_length - L1 - best_individual[0]], color='yellow', s=100, label='Best L3')

    axs[2].set_ylabel('L3', color='red')
    axs[2].set_xlabel('Individual Index')
    axs[2].legend(loc='upper left')

    axs[0].set_title(f'Final Generation ({generations}) Population Solutions')

    # Plot L1, L2, L3 over generations
    generations_list = range(1, len(best_performers) + 1)
    a_values = [ind[0][0] for ind in best_performers]
    b_values = [ind[0][1] for ind in best_performers]
    c_values = [ind[0][2] for ind in best_performers]
    fig_lengths, ax = plt.subplots()
    ax.plot(generations_list, a_values, label='L1', color='blue')
    ax.plot(generations_list, b_values, label='L2', color='green')
    ax.plot(generations_list, c_values, label='L3', color='red')
    ax.set_xlabel('Generation')
    ax.set_ylabel('Lengths')
    ax.set_title('Lengths Over Generations')
    ax.legend()

    # Plot delta-V over generations
    best_fitness_values = [fit[1] for fit in best_performers]
    min_fitness_values = [min([fitness_function_fixed_L1(ind, L1, rocket_length) for ind in population]) for population in all_populations]
    max_fitness_values = [max([fitness_function_fixed_L1(ind, L1, rocket_length) for ind in population]) for population in all_populations]
    fig_fitness, ax = plt.subplots()
    ax.plot(generations_list, best_fitness_values, label='Best Fitness', color='black')
    ax.fill_between(generations_list, min_fitness_values, max_fitness_values, color='gray', alpha=0.5,
                    label='Fitness Range')
    ax.set_xlabel('Generation')
    ax.set_ylabel('Delta V')
    ax.set_title('Delta V Over Generations')
    ax.legend()

    return max(population, key=lambda ind: fitness_function_fixed_L1(ind, L1, rocket_length)), [fig, fig_lengths, fig_fitness]
