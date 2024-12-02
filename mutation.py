import numpy as np
from const import MASS_LOWER_BOUND, MASS_UPPER_BOUND, ELASTICITY_LOWER_BOUND, ELASTICITY_UPPER_BOUND, FRICTION_LOWER_BOUND, FRICTION_UPPER_BOUND

# Mutate all the parameters of the wheel by an amount
# the shape of the wheel changes with a small probability
def mutate_full_wheel(wheel_matrix):
    n, d = wheel_matrix.shape
    vertex_mutation_rate = 0.0005
    property_mutation_rate = 0.1

    for i in range(n-1):
        for j in range(d):
            if np.random.rand() < vertex_mutation_rate:
                if (wheel_matrix[i][j] == 0):
                    wheel_matrix[i][j] = 1
                else:
                    wheel_matrix[i][j] = 0

    #MASS
    if np.random.rand() < property_mutation_rate:
        new_value = wheel_matrix[-1][0] * 0.95 if np.random.rand() < 0.5 else 1.05
        wheel_matrix[-1][0] = min(MASS_UPPER_BOUND, max(MASS_LOWER_BOUND, new_value))

    #FRICTION
    if np.random.rand() < property_mutation_rate:
        new_value = wheel_matrix[-1][1] * 0.95 if np.random.rand() < 0.5 else 1.05
        wheel_matrix[-1][1] = min(FRICTION_UPPER_BOUND, max(FRICTION_LOWER_BOUND, new_value))
     
    #ELASTICITY
    if np.random.rand() < property_mutation_rate:
        new_value = wheel_matrix[-1][2] * 0.95 if np.random.rand() < 0.5 else 1.05
        wheel_matrix[-1][2] = min(ELASTICITY_UPPER_BOUND, max(ELASTICITY_LOWER_BOUND, new_value))

                    
