import numpy as np
import pymunk
import sys

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        # Allow KeyboardInterrupt to exit the program
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    print(f"Uncaught exception: {exc_value}")
    raise Exception("sys except")

sys.excepthook = handle_exception

class Wheel():
    def __init__(self, mass, friction, elasticity, matrix, position=(0, 0)):
        self.mass = mass
        self.vertices = vertices_from_matrix(matrix)
        self.matrix = matrix
        self.moment = pymunk.moment_for_poly(mass, self.vertices)

        if self.moment < 0:
            raise Exception("Negative moment")

        self.body = pymunk.Body(mass, self.moment)
        self.body.position = position
        self.shape = pymunk.Poly(self.body, vertices=self.vertices, radius=0)
        self.shape.friction = friction
        self.shape.elasticity = elasticity

    def get_raw_data(self):
        # other_data = np.zeros(1, self.matrix.shape[0])
        # other_data[0] = self.mass
        # other_data[1] = self.friction
        # other_data[2] = self.elasticity
        # data = np.concatenate((other_data, self.matrix), axis=1)

        return self.matrix

def generate_wheel_matrix():
    matrix = np.zeros((100, 100), dtype=float)
    vertex_probability = 0.005

    for y in range(matrix.shape[0]):
        for x in range(matrix.shape[1]):
            if np.random.rand() < vertex_probability:
                matrix[x][y] = 1

    return matrix

def vertices_from_matrix(representation):
    vertices = [(int(x) - 50, int(y) - 50) for x, y in zip(np.where(representation == 1)[0], np.where(representation == 1)[1])]
    
    if len(vertices) < 3:
        raise Exception("Not enough vertices")
    
    return vertices

if __name__ == '__main__':
    mat = generate_wheel_matrix()
    print(mat)
    print(vertices_from_matrix(mat))
    wheel = Wheel(1, 0.5, 0.1, vertices_from_matrix(mat))
