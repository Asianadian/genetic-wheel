import random
import numpy as np
from const import NUM_PROPERTIES

def genetic(wheel_matrix_1, wheel_matrix_2):
    structure_matrix_1, structure_matrix_2 = wheel_matrix_1[:-1], wheel_matrix_2[:-1]
    out_structure_matrix = genetic_split_structure(structure_matrix_1, structure_matrix_2)

    property_matrix_1, property_matrix_2 = wheel_matrix_1[-1], wheel_matrix_2[-1]
    out_property_matrix = genetic_mean_properties(property_matrix_1, property_matrix_2)

    return np.concatenate([out_structure_matrix, out_property_matrix])

def genetic_split_structure(structure_matrix_1, structure_matrix_2):
    n, d = structure_matrix_1.shape
    
    split = random.randrange(0, n)
    g1 = structure_matrix_1[:split]
    g2 = structure_matrix_2[split:n]
    structure_matrix = np.concatenate([g1, g2])

    return structure_matrix

def genetic_split_structure_by_row(structure_matrix_1, structure_matrix_2):
    n, d = structure_matrix_1.shape
    
    structure_matrix = np.zeros((n, d))
    for row in range(n):
        split = random.randrange(0, d)
        structure_matrix[row][:split] = structure_matrix_1[row][:split]
        structure_matrix[row][split:] = structure_matrix_2[row][split:]

    return structure_matrix

def genetic_split_structure_by_element(structure_matrix_1, structure_matrix_2):
    n, d = structure_matrix_1.shape

    structure_matrix = np.zeros((n, d))
    for row in range(n):
        for col in range(d):
            structure_matrix[row][col] = structure_matrix_1[row][col] if np.random.rand() < 0.5 else structure_matrix_2[row][col]

    return structure_matrix

def genetic_split_properties(property_matrix_1, property_matrix_2):
    property_matrix = np.zeros_like(property_matrix_1)

    split = random.randrange(0, NUM_PROPERTIES)
    property_matrix[:split] = property_matrix_1[:split]
    property_matrix[split:] = property_matrix_2[split:]

    return property_matrix[:, None].T

def genetic_split_properties_by_property(property_matrix_1, property_matrix_2):
    property_matrix = np.zeros_like(property_matrix_1)

    for i in range(NUM_PROPERTIES):
        property_matrix[i] = property_matrix_1[i] if np.random.rand() < 0.5 else property_matrix_2[i]

    return property_matrix[:, None].T

def genetic_mean_properties(property_matrix_1, property_matrix_2):
    property_matrix = (property_matrix_1 + property_matrix_2)/2

    return property_matrix[:, None].T





