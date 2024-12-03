import represention
import genetic
import mutation
import fitness
from matplotlib import pyplot as plt
from const import NUM_PROPERTIES, POPULATION_SIZE, NUM_ITERATIONS, NUM_OFFSPRING

import random

import numpy as np
import sys

def plot_averate_properties_per_generation(avg_properties_per_generation):
  gen = len(avg_fitness_per_generation)

  mass = avg_properties_per_generation[:, 0]
  friction = avg_properties_per_generation[:, 1]
  elasticity = avg_properties_per_generation[:, 2]

  # Create a plot
  plt.plot(mass, label='Mass', color='r')
  plt.plot(friction, label='Friction', color='g')
  plt.plot(elasticity, label='Elasticity', color='b')

  # Add labels and title
  plt.xlabel('Generation')
  plt.ylabel('Avg Property Value')
  plt.title('Evolution of Properties per Generation')

  # Display grid for better readability
  plt.grid(True)

  # Add a legend to differentiate the lines
  plt.legend()

  plt.xticks(np.arange(0, gen, 10))

  # Show the plot
  plt.savefig('AVG_P.png')
  plt.show()

def plot_max_fitness_per_generation(max_fitness_per_generation):
  gen = len(avg_fitness_per_generation)

  # Create a plot
  plt.plot(max_fitness_per_generation, marker='o', color='b', linestyle='-', markersize=6)

  # Add labels and title
  plt.xlabel('Generation')
  plt.ylabel('Max Fitness')
  plt.title('Max Fitness per Generation')

  # Display grid for better readability
  plt.grid(True)

  plt.xticks(np.arange(0, gen, 10))

  # Show the plot
  plt.savefig('MAX_F.png')
  plt.show()

def plot_average_fitness_per_generation(avg_fitness_per_generation):
  gen = len(avg_fitness_per_generation)

  # Create a plot
  plt.plot(avg_fitness_per_generation, marker='o', color='b', linestyle='-', markersize=6)

  # Add labels and title
  plt.xlabel('Generation')
  plt.ylabel('Avg Fitness')
  plt.title('Avg Fitness per Generation')

  # Display grid for better readability
  plt.grid(True)

  plt.xticks(np.arange(0, gen, 10))

  # Show the plot
  plt.savefig('AVG_F.png')
  plt.show()

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        # Allow KeyboardInterrupt to exit the program
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    print(f"Uncaught exception: {exc_value}")
    raise Exception("System exception")

sys.excepthook = handle_exception

def genetic_algorithm(population, num_iterations, offspring_per_generation, genetic_structure_function, genetic_property_function, snapshots=False, graphs=False):
  
  max_fitness_wheel_per_generation = []

  max_fitness_per_generation = np.zeros(num_iterations)
  avg_fitness_per_generation = np.zeros(num_iterations)
  avg_properties_per_generation = np.zeros((num_iterations, NUM_PROPERTIES))

  for gen in range(num_iterations):
    print('Generation', gen)
    properties_this_generation = np.zeros((POPULATION_SIZE, NUM_PROPERTIES))

    population_fitness = np.zeros(POPULATION_SIZE)
    for i, p in enumerate(population):
      population_fitness[i] = fitness.fitness_distance(p)
      properties_this_generation[i] = p[-1][:3]

    max_fitness_wheel_per_generation.append(population[np.argmax(population_fitness)])

    if graphs:
      max_fitness_per_generation[gen] = np.max(population_fitness)
      avg_fitness_per_generation[gen] = np.mean(population_fitness)
      avg_properties_per_generation[gen] = np.mean(properties_this_generation, axis=0)

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
      curr_offspring = genetic.genetic(parent_a, parent_b, genetic_structure_function, genetic_property_function)
      mutation.mutate_full_wheel(curr_offspring)
      offspring.append(curr_offspring)


    deceased_indices = np.random.choice([i for i in range(len(population))], offspring_per_generation, False, p=population_fitness_prob_inv)
    for deceased_index in sorted(deceased_indices, reverse=True):
      del population[deceased_index]

    population = population + offspring

  return population, max_fitness_wheel_per_generation, max_fitness_per_generation, avg_fitness_per_generation, avg_properties_per_generation

population = [represention.random_wheel_data() for _ in range(POPULATION_SIZE)]

for genetic_structure_function in genetic.GENETIC_STRUCTURE_FUNCTIONS:
    for genetic_property_function in genetic.GENETIC_PROPERTY_FUNCTIONS:
        population, max_fitness_wheel_per_generation, max_fitness_per_generation, avg_fitness_per_generation, avg_properties_per_generation = genetic_algorithm(population, NUM_ITERATIONS, NUM_OFFSPRING, genetic_structure_function, genetic_property_function, graphs=True)

        # show results
        fitness.visualize(max_fitness_wheel_per_generation)
        plot_max_fitness_per_generation(max_fitness_per_generation)
        plot_average_fitness_per_generation(avg_fitness_per_generation)
        plot_averate_properties_per_generation(avg_properties_per_generation)

# population_fitness = np.zeros(POPULATION_SIZE)
# for i, p in enumerate(population):
#     population_fitness[i] = fitness.fitness_distance(p)

# best = np.argmax(population_fitness)

# print(fitness.fitness_distance_visualize(population[best]))
# print(population_fitness[best])
# print(population[best])
# fitness.draw_wheel_polygon(population[best])