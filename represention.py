import numpy as np
import pymunk

class Wheel():
    def __init__(self, mass, friction, elasticity, matrix, position=(0, 0)):
        self.mass = mass
        self.position = position
        self.vertices = vertices_from_matrix(matrix)
        self.matrix = matrix
        self.moment = pymunk.moment_for_poly(mass, self.vertices)
        self.body = pymunk.Body(mass, self.moment)
        self.body.position = position
        self.shape = pymunk.Poly(self.body, self.vertices)
        self.shape.friction = friction
        self.shape.elasticity = elasticity

    def get_raw_data(self):
        other_data = np.zeros((1, 100))
        other_data[0][0] = self.mass
        other_data[0][1] = self.shape.friction
        other_data[0][2] = self.shape.elasticity
        return np.concatenate(self.matrix, other_data, axis=1)

def generate_wheel_matrix():
    matrix = np.zeros((100, 100), dtype=float)
    vertex_probability = 0.01

    for y in range(matrix.shape[0]):
        for x in range(matrix.shape[1]):
            if np.random.rand() < vertex_probability:
                matrix[x][y] = 1

    return matrix

def vertices_from_matrix(representation):
    return [(int(x) - 50, int(y) - 50) for x, y in zip(np.where(representation == 1)[0], np.where(representation == 1)[1])]

if __name__ == '__main__':
    mat = generate_wheel_matrix()
    print(mat)
    print(vertices_from_matrix(mat))
    wheel = Wheel(1, 0.5, 0.1, vertices_from_matrix(mat))
