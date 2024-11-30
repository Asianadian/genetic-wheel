import random
import numpy as np

def genetic_split_row(x, y):
    n, d = x.shape
    split = random.randrange(1, n)

    g1 = x[:split]
    g2 = y[split:]
    matrix = np.concatenate([g1, g2])

    # split = random.randrange(0, 1)
    # properties = 

    return matrix

def genetic_split_col(x, y):
    n, d = x.shape

    for row in range(n):
        split = random.randrange(1, d)

        x[row][split:] = y[row][split:]

    return x

# print(genetic_split_col(np.array([[1,2,3,4,5], [1,2,3,4,5], [1,2,3,4,5], [1,2,3,4,5], [1,2,3,4,5], [1,2,3,4,5], [1,2,3,4,5], [1,2,3,4,5]]), np.array([[6,7,8,9,10], [6,7,8,9,10], [6,7,8,9,10], [6,7,8,9,10], [6,7,8,9,10], [6,7,8,9,10], [6,7,8,9,10], [6,7,8,9,10]])))


