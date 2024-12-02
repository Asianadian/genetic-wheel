import represention
import genetic
import mutation
import fitness

import random

import numpy as np
import sys

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        # Allow KeyboardInterrupt to exit the program
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    print(f"Uncaught exception: {exc_value}")
    raise Exception("System exception")

sys.excepthook = handle_exception

POPULATION_SIZE = 500

def genetic_algorithm(population, num_iterations, offspring_per_generation, snapshots=False, graph=False):
  max_fitness_per_generation = []
  for i in range(num_iterations):
    print('Generation', i)
    population_fitness = np.zeros(POPULATION_SIZE)
    for i, p in enumerate(population):
      population_fitness[i] = fitness.fitness_distance(p)

    max_fitness_per_generation.append(population[np.argmax(population_fitness)])

    sum_fitness = np.sum(population_fitness)
    population_fitness_prob = population_fitness / sum_fitness

    population_fitness_prob_inv = 1/population_fitness_prob
    sum_prob = np.sum(population_fitness_prob_inv)
    population_fitness_prob_inv = population_fitness_prob_inv / sum_prob

    # TODO:no replace all 
    offspring = []
    for o in range(offspring_per_generation):
      parent_a_i, parent_b_i = np.random.choice([i for i in range(len(population))], 2, False, p=population_fitness_prob)
      parent_a, parent_b = population[parent_a_i], population[parent_b_i]
      curr_offspring = genetic.genetic(parent_a, parent_b)
      mutation.mutate_full_wheel(curr_offspring)
      offspring.append(curr_offspring)


    deceased_indices = np.random.choice([i for i in range(len(population))], offspring_per_generation, False, p=population_fitness_prob_inv)
    for deceased_index in sorted(deceased_indices, reverse=True):
      del population[deceased_index]

    population = population + offspring

  return population, max_fitness_per_generation

population = [represention.random_wheel_data() for _ in range(POPULATION_SIZE)]

population, max_fitness_per_generation = genetic_algorithm(population, 100, 100)

print(len(max_fitness_per_generation))
fitness.visualize(max_fitness_per_generation)

# population_fitness = np.zeros(POPULATION_SIZE)
# for i, p in enumerate(population):
#     population_fitness[i] = fitness.fitness_distance(p)

# best = np.argmax(population_fitness)

# print(fitness.fitness_distance_visualize(population[best]))
# print(population_fitness[best])
# print(population[best])
# fitness.draw_wheel_polygon(population[best])