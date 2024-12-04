from matplotlib import pyplot as plt
import numpy as np

def plot_averate_properties_per_generation(avg_properties_per_generation, meta_data='', show=False):
  gen = len(avg_properties_per_generation)

  mass = avg_properties_per_generation[:, 0]
  friction = avg_properties_per_generation[:, 1]
  elasticity = avg_properties_per_generation[:, 2]

  plt.plot(mass, label='Mass', color='r')
  plt.plot(friction, label='Friction', color='g')
  plt.plot(elasticity, label='Elasticity', color='b')

  plt.xlabel('Generation')
  plt.ylabel('Avg Property Value')
  plt.title('Evolution of Properties per Generation')

  plt.grid(True)

  plt.legend()

  plt.xticks(np.arange(0, gen, 10))

  plt.savefig(f'logs/AVG_P{meta_data}.png')
  if show:
    plt.show()
  else:
    plt.clf()

def plot_max_fitness_per_generation(max_fitness_per_generation, meta_data='', show=False):
  gen = len(max_fitness_per_generation)

  plt.plot(max_fitness_per_generation, marker='o', color='b', linestyle='-', markersize=6)

  plt.xlabel('Generation')
  plt.ylabel('Max Fitness')
  plt.title('Max Fitness per Generation')

  plt.grid(True)

  plt.xticks(np.arange(0, gen, 10))

  plt.savefig(f'logs/MAX_F{meta_data}.png')
  if show:
    plt.show()
  else:
    plt.clf()

def plot_average_fitness_per_generation(avg_fitness_per_generation, meta_data='', show=False):
  gen = len(avg_fitness_per_generation)

  plt.plot(avg_fitness_per_generation, marker='o', color='b', linestyle='-', markersize=6)

  plt.xlabel('Generation')
  plt.ylabel('Avg Fitness')
  plt.title('Avg Fitness per Generation')

  plt.grid(True)

  plt.xticks(np.arange(0, gen, 10))

  plt.savefig(f'logs/AVG_F{meta_data}.png')
  if show:
    plt.show()
  else:
    plt.clf()