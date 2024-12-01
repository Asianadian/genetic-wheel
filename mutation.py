import numpy as np

# Mutate all the parameters of the wheel by an amount
# the shape of the wheel changes with a small probability
def mutate_full_wheel(wheel_matrix):
    n, d = wheel_matrix.shape
    vertex_mutation_rate = 0.0005
    property_mutation_rate = 0.01

    for i in range(n-1):
        for j in range(d):
            if np.random.rand() < vertex_mutation_rate:
                if (wheel_matrix[i][j] == 0):
                    wheel_matrix[i][j] = 1
                else:
                    wheel_matrix[i][j] = 0

    for i in range(1, 3):
        new_value = wheel_matrix[-1][i] + (np.random.uniform(0, property_mutation_rate) - (property_mutation_rate / 2))
        if new_value > 0 and new_value < 1:
            wheel_matrix[-1][i] = new_value
                    
