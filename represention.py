import numpy as np

def init_representation():
    matrix = np.zeros((100, 100))

    for y in range(matrix.shape[0]):
        for x in range(matrix.shape[1]):
            if np.random.rand() < 0.01:
                matrix[x][y] = 1
    #print(matrix)
    return matrix


def get_coordinates(representation):
    return [(int(x) - 50, int(y) - 50) for x, y in zip(np.where(representation == 1)[0], np.where(representation == 1)[1])]

if __name__ == '__main__':
    rep = init_representation()
    print(rep)
    print(get_coordinates(rep))


