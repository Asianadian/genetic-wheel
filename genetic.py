import random
import numpy as np

def genetic_split_row(x, y):
    n, d = x.shape
    
    # build n row matrix with 0-split from x and split-n from y
    split = random.randrange(1, n)
    g1 = x[:split]
    g2 = y[split:n+1]
    wheel_matrix = np.concatenate([g1, g2])

    properties = genetic_split_properties(x, y)

    return np.concatenate([wheel_matrix, properties], axis=1)

def genetic_split_col(x, y):
    n, d = x.shape
    num_other_properties = 3

    # build n row matrix where a split amount of values are taken from x
    # and n-split values are taken from y
    for row in range(n):
        split = random.randrange(1, d)
        x[row][split:] = y[row][split:]

    # pick the midpoint randomly offset 
    # works out to index 1 or 2
    split = (num_other_properties // 2) + random.randrange(0, 1)
    properties = np.concatenate([x[n+1][:split], y[n+1][split]], axis=0)

    return x

def genetic_split_properties(x, y):
    num_other_properties = 3

    # pick the midpoint randomly offset 
    # works out to index 1 or 2
    split = (num_other_properties // 2) + random.randrange(0, 1)
    x = np.concatenate([x[n+1][:split], y[n+1][split]], axis=0)

    return x

# print(genetic_split_col(np.array([[1,2,3,4,5], [1,2,3,4,5], [1,2,3,4,5], [1,2,3,4,5], [1,2,3,4,5], [1,2,3,4,5], [1,2,3,4,5], [1,2,3,4,5]]), np.array([[6,7,8,9,10], [6,7,8,9,10], [6,7,8,9,10], [6,7,8,9,10], [6,7,8,9,10], [6,7,8,9,10], [6,7,8,9,10], [6,7,8,9,10]])))


