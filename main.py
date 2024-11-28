import represention
import genetic
import mutation
import fitness

import random

import numpy as np

POPULATION_SIZE = 500

def genetic_algorithm(population, num_iterations, offspring_per_generation):
  for i in range(num_iterations):
    print(i)
    population_fitness = np.zeros(POPULATION_SIZE)
    for i, p in enumerate(population):
      population_fitness[i] = fitness.fitness_distance(p)

    sum_fitness = np.sum(population_fitness)
    population_fitness_prob = population_fitness / sum_fitness

    population_fitness_prob_inv = 1/population_fitness_prob
    sum_prob = np.sum(population_fitness_prob_inv)
    population_fitness_prob_inv = population_fitness_prob_inv / sum_prob

    # if max(population_fitness) > THRESHOLD:
    #   optimal_index = argmax(population_fitness)
    #   return population[optimal_index]

    # TODO:no replace all 
    offspring = []
    for o in range(offspring_per_generation):
      parent_a_i, parent_b_i = np.random.choice([i for i in range(len(population))], 2, False, p=population_fitness_prob)
      parent_a, parent_b = population[parent_a_i], population[parent_b_i]
      curr_offspring = genetic.genetic_split_row(parent_a, parent_b)
      curr_offspring = mutation.mutate_full_wheel(curr_offspring)
      offspring.append(curr_offspring)


    deceased_indices = np.random.choice([i for i in range(len(population))], offspring_per_generation, False, p=population_fitness_prob_inv)
    for deceased_index in sorted(deceased_indices, reverse=True):
      del population[deceased_index]

    population = population + offspring

  return population

population = [represention.generate_wheel_matrix() for _ in range(POPULATION_SIZE)]

population = genetic_algorithm(population, 100, 100)

population_fitness = np.zeros(POPULATION_SIZE)
for i, p in enumerate(population):
    population_fitness[i] = fitness.fitness_distance(p)

best = np.argmax(population_fitness)

fitness.fitness_distance_visualize(population[best])