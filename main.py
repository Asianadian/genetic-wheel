from const import NUM_PROPERTIES
from const import NUM_PROPERTIES, POPULATION_SIZE, NUM_ITERATIONS, NUM_OFFSPRING
from plot import plot_average_fitness_per_generation, plot_max_fitness_per_generation, plot_averate_properties_per_generation
import fitness
import genetic
import mutation
import numpy as np
import represention
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor

'''
Exception handling for Chipmunk2D 

pymunk terminates the program instead of throwing exceptions in some cases
'''
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        # Allow KeyboardInterrupt to exit the program
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    print(f"Uncaught exception: {exc_value}")
    raise Exception("System exception")
sys.excepthook = handle_exception

def genetic_algorithm(population, num_iterations, offspring_per_generation, genetic_structure_function, genetic_property_function, graphs=False):
  population_size = len(population)
  max_fitness_wheel_per_generation = []

  max_fitness_per_generation = np.zeros(num_iterations)
  avg_fitness_per_generation = np.zeros(num_iterations)
  avg_properties_per_generation = np.zeros((num_iterations, NUM_PROPERTIES))

  for gen in range(num_iterations):
    print('Generation:', gen)
    properties_this_generation = np.zeros((population_size, NUM_PROPERTIES))

    population_fitness = np.zeros(population_size)
    for i, p in enumerate(population):
      population_fitness[i] = fitness.fitness_distance(p)
      properties_this_generation[i] = p[-1][:3]

    max_fitness_wheel_per_generation.append(population[np.argmax(population_fitness)])

    if graphs:
      max_fitness_per_generation[gen] = np.max(population_fitness)
      avg_fitness_per_generation[gen] = np.mean(population_fitness)
      avg_properties_per_generation[gen] = np.mean(properties_this_generation, axis=0)

    # Give representations probability proportion to fitness
    sum_fitness = np.sum(population_fitness)
    population_fitness_prob = population_fitness / sum_fitness

    # Create new offspring
    offspring = []
    for _ in range(offspring_per_generation):
      parent_a_i, parent_b_i = np.random.choice([i for i in range(len(population))], 2, False, p=population_fitness_prob)
      parent_a, parent_b = population[parent_a_i], population[parent_b_i]
      curr_offspring = genetic.genetic(parent_a, parent_b, genetic_structure_function, genetic_property_function)
      mutation.mutate_full_wheel(curr_offspring)
      offspring.append(curr_offspring)

    # Give representations probability inversely proportional to fitness
    population_fitness_prob_inv = 1/population_fitness_prob
    sum_prob = np.sum(population_fitness_prob_inv)
    population_fitness_prob_inv = population_fitness_prob_inv / sum_prob

    # Kill off unfit representations
    deceased_indices = np.random.choice([i for i in range(len(population))], offspring_per_generation, False, p=population_fitness_prob_inv)
    for deceased_index in sorted(deceased_indices, reverse=True):
      del population[deceased_index]

    population = population + offspring

  return population, max_fitness_wheel_per_generation, max_fitness_per_generation, avg_fitness_per_generation, avg_properties_per_generation

'''
Testing environment for genetic algorithm

Runs genetic algorithm with all variations of genetic functions and visualizes results
'''
def run_experiments():
    runs = []

    for s, genetic_structure_function in enumerate(genetic.GENETIC_STRUCTURE_FUNCTIONS):
        for p, genetic_property_function in enumerate(genetic.GENETIC_PROPERTY_FUNCTIONS):
            runs.append(run_experiment_for_combination(s, p, genetic_structure_function, genetic_property_function))

    
    for s, genetic_structure_function in enumerate(genetic.GENETIC_STRUCTURE_FUNCTIONS):
        for p, genetic_property_function in enumerate(genetic.GENETIC_PROPERTY_FUNCTIONS):
            fitness.visualize(runs[s*len(genetic.GENETIC_PROPERTY_FUNCTIONS) + p], meta_data=f'_{genetic_structure_function.__name__}_{genetic_property_function.__name__}')
'''
Runs genetic algorithm with given genetic functions and visualizes results
'''
def run_experiment_for_combination(s, p, genetic_structure_function, genetic_property_function):
    start = time.time()
    population = [represention.random_wheel_data() for _ in range(POPULATION_SIZE)]
    population, max_fitness_wheel_per_generation, max_fitness_per_generation, avg_fitness_per_generation, avg_properties_per_generation = genetic_algorithm(population, NUM_ITERATIONS, NUM_OFFSPRING, genetic_structure_function, genetic_property_function, graphs=True)

    # Show results
    print(f'[{s}|{p}] took {time.time() - start} seconds')
    # fitness.visualize(max_fitness_wheel_per_generation, meta_data=f'[{s}|{p}]')
    plot_max_fitness_per_generation(max_fitness_per_generation, meta_data=f'_{s}_{p}')
    plot_average_fitness_per_generation(avg_fitness_per_generation, meta_data=f'_{s}_{p}')
    plot_averate_properties_per_generation(avg_properties_per_generation, meta_data=f'_{s}_{p}')

    return max_fitness_wheel_per_generation

'''
Demo function for live genetic algorithm showcase

Runs genetic algorithm with given parameters and visualizes results
'''
def demo(pop_size, num_iter, num_offspring, genetic_structure_function, genetic_property_function):
    start = time.time()
    population = [represention.random_wheel_data() for _ in range(pop_size)]
    population, max_fitness_wheel_per_generation, max_fitness_per_generation, avg_fitness_per_generation, avg_properties_per_generation = genetic_algorithm(population, num_iter, num_offspring, genetic_structure_function, genetic_property_function, graphs=True)

    # show results
    print(f'took {time.time() - start} seconds with {pop_size} population size, {num_iter} iterations, {num_offspring} offspring')
    print(f'genetic_structure_function: {genetic_structure_function.__name__}, genetic_property_function: {genetic_property_function.__name__}')
    fitness.visualize(max_fitness_wheel_per_generation)
    plot_max_fitness_per_generation(max_fitness_per_generation, meta_data=f'_demo', show=True)
    plot_average_fitness_per_generation(avg_fitness_per_generation, meta_data=f'_demo', show=True)
    plot_averate_properties_per_generation(avg_properties_per_generation, meta_data=f'_demo', show=True)

if __name__ == '__main__':
    run_experiments()
    
    # # uncomment for demo 
    # population_size = 200
    # num_iterations = 100
    # num_offspring = 40
    # # choice between: genetic_split_structure, genetic_split_structure_by_row, genetic_split_structure_by_element
    # genetic_structure_function = genetic.genetic_split_structure
    # # genetic_split_properties, genetic_split_properties_by_property, genetic_mean_properties
    # genetic_property_function = genetic.genetic_split_properties
    # demo(population_size, num_iterations, num_offspring, genetic_structure_function, genetic_property_function)