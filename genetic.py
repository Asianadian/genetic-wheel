from const import NUM_PROPERTIES
import numpy as np
import random

'''
Generic genetic function

Uses a genetic function on the structure and a genetic function on the properties

Returns new representation
'''
def genetic(wheel_matrix_1, wheel_matrix_2, genetic_structure_function, genetic_property_function):
    structure_matrix_1, structure_matrix_2 = wheel_matrix_1[:-1], wheel_matrix_2[:-1]
    out_structure_matrix = genetic_structure_function(structure_matrix_1, structure_matrix_2)

    property_matrix_1, property_matrix_2 = wheel_matrix_1[-1], wheel_matrix_2[-1]
    out_property_matrix = genetic_property_function(property_matrix_1, property_matrix_2)

    return np.concatenate([out_structure_matrix, out_property_matrix])

'''
Genetic function for structure

Chooses a row number, takes all rows before that number from the first matrix, and all remaining rows from the second matrix

Returns the concatenation of those rows
'''
def genetic_split_structure(structure_matrix_1, structure_matrix_2):
    n, d = structure_matrix_1.shape
    
    split = random.randrange(0, n)
    g1 = structure_matrix_1[:split]
    g2 = structure_matrix_2[split:n]
    structure_matrix = np.concatenate([g1, g2])

    return structure_matrix

'''
Genetic function for structure

For each row
    Chooses a column number, takes all elements before that number from the row, and all remaining elements from the second matrix

Returns the concatenation of those rows
'''
def genetic_split_structure_by_row(structure_matrix_1, structure_matrix_2):
    n, d = structure_matrix_1.shape
    
    structure_matrix = np.zeros((n, d))
    for row in range(n):
        split = random.randrange(0, d)
        structure_matrix[row][:split] = structure_matrix_1[row][:split]
        structure_matrix[row][split:] = structure_matrix_2[row][split:]

    return structure_matrix

'''
Genetic function for structure

For each element
    Choose element from first matrix with probability 50%, otherwise choose element from second matrix

Returns the concatenation of those elements
'''
def genetic_split_structure_by_element(structure_matrix_1, structure_matrix_2):
    n, d = structure_matrix_1.shape

    structure_matrix = np.zeros((n, d))
    for row in range(n):
        for col in range(d):
            structure_matrix[row][col] = structure_matrix_1[row][col] if np.random.rand() < 0.5 else structure_matrix_2[row][col]

    return structure_matrix

'''
Genetic function for properties

Choose a column number, take all properties before that number from the first matrix, and all remaining properties from the second matrix

Returns the concatenation of properties
'''
def genetic_split_properties(property_matrix_1, property_matrix_2):
    property_matrix = np.zeros_like(property_matrix_1)

    split = random.randrange(0, NUM_PROPERTIES)
    property_matrix[:split] = property_matrix_1[:split]
    property_matrix[split:] = property_matrix_2[split:]

    return property_matrix[:, None].T

'''
Genetic function for properties

For each property
    Choose property from the first matrix with probability 50%, otherwise choose element from second matrix

Returns the concatenation of properties
'''
def genetic_split_properties_by_property(property_matrix_1, property_matrix_2):
    property_matrix = np.zeros_like(property_matrix_1)

    for i in range(NUM_PROPERTIES):
        property_matrix[i] = property_matrix_1[i] if np.random.rand() < 0.5 else property_matrix_2[i]

    return property_matrix[:, None].T

'''
Genetic function for properties

Returns the mean of all properties
'''
def genetic_mean_properties(property_matrix_1, property_matrix_2):
    property_matrix = (property_matrix_1 + property_matrix_2)/2

    return property_matrix[:, None].T

GENETIC_STRUCTURE_FUNCTIONS = [genetic_split_structure, genetic_split_structure_by_row, genetic_split_structure_by_element]
GENETIC_PROPERTY_FUNCTIONS = [genetic_split_properties, genetic_split_properties_by_property, genetic_mean_properties]



