import numpy as np

# Mutate all the parameters of the wheel by an amount
# the shape of the wheel changes with a small probability
def mutate_full_wheel(wheel_matrix):
    vertex_mutation_rate = 0.0001

    for i in range(wheel_matrix.shape[0]):
        for j in range(wheel_matrix.shape[1]):
            if np.random.rand() < vertex_mutation_rate:
                if (wheel_matrix[i][j] == 0):
                    wheel_matrix[i][j] = 1
                else:
                    wheel_matrix[i][j] = 0

    # for i in range(3):
    #     wheel_matrix[101][i] = wheel_matrix[101][i] + np.random.rand() * 0.1 - 0.05
                    
