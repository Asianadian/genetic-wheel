import numpy as np
import pymunk
import sys
from const import MASS_LOWER_BOUND, MASS_UPPER_BOUND, ELASTICITY_LOWER_BOUND, ELASTICITY_UPPER_BOUND, FRICTION_LOWER_BOUND, FRICTION_UPPER_BOUND
from scipy.spatial import ConvexHull

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
        self.shape.filter = pymunk.ShapeFilter(group=2)

    def get_raw_data(self):
        other_data = np.zeros((1, self.matrix.shape[0]), dtype=float)
        other_data[0][0] = self.mass
        other_data[0][1] = self.friction
        other_data[0][2] = self.elasticity
        data = np.concatenate([self.matrix, other_data])

        return data

def wheel_from_raw_data(data, position=(0, 0)):
    matrix = data[:-1]
    mass = data[-1][0]
    friction = data[-1][1]
    elasticity = data[-1][2]
    return Wheel(mass, friction, elasticity, matrix, position)

def generate_wheel_matrix():
    matrix = np.zeros((100, 100), dtype=float)
    vertex_probability = 0.005

    for y in range(matrix.shape[0]):
        for x in range(matrix.shape[1]):
            if np.random.rand() < vertex_probability:
                matrix[x][y] = 1

    return matrix

def random_wheel_data():
    matrix = generate_wheel_matrix()
    other_data = np.zeros((1, matrix.shape[1]), dtype=float)
    other_data[0][0] = np.random.uniform(MASS_LOWER_BOUND, MASS_UPPER_BOUND)
    other_data[0][1] = np.random.uniform(FRICTION_LOWER_BOUND, FRICTION_UPPER_BOUND)
    other_data[0][2] = np.random.uniform(ELASTICITY_LOWER_BOUND, ELASTICITY_UPPER_BOUND)
    
    return np.concatenate([matrix, other_data])

def vertices_from_matrix(representation):
    vertices = [(int(x), int(y)) for x, y in zip(np.where(representation == 1)[0], np.where(representation == 1)[1])]
    vertices = get_convex_hull(vertices)
    centroid = calculate_centroid(vertices)
    
    for i in range(len(vertices)):
        vertices[i] = (vertices[i][0] - centroid[0], vertices[i][1] - centroid[1])
    
    if len(vertices) < 3:
        raise Exception("Not enough vertices")
    
    return vertices

def get_convex_hull(vertices):

    if len(vertices) < 3:
        raise ValueError("At least 3 vertices are required to calculate a convex hull")
    
    # Convert vertices to a NumPy array
    points = np.array(vertices)
    
    # Compute the convex hull
    hull = ConvexHull(points)
    
    # Extract the vertices of the hull in counterclockwise order
    hull_vertices = [tuple(points[vertex]) for vertex in hull.vertices]
    
    return hull_vertices

def calculate_centroid(vertices):
    """
    Calculate the centroid of a polygon given its vertices.
    
    Parameters:
    vertices (list of tuples): List of (x, y) tuples representing the vertices of the polygon.
    
    Returns:
    tuple: (x, y) coordinates of the centroid.
    """
    if len(vertices) < 3:  # A polygon must have at least three vertices
        raise ValueError("A polygon must have at least three vertices.")
    
    # Ensure the polygon is closed by appending the first vertex at the end
    vertices = vertices + [vertices[0]]
    
    # Compute the centroid
    A = 0  # Area of the polygon
    Cx = 0
    Cy = 0
    for i in range(len(vertices) - 1):
        x0, y0 = vertices[i]
        x1, y1 = vertices[i + 1]
        common_factor = (x0 * y1 - x1 * y0)
        A += common_factor
        Cx += (x0 + x1) * common_factor
        Cy += (y0 + y1) * common_factor
    
    A *= 0.5
    if A == 0:  # To avoid division by zero
        raise ValueError("The vertices do not form a valid polygon (zero area).")
    
    Cx /= (6 * A)
    Cy /= (6 * A)
    return (Cx, Cy)


if __name__ == '__main__':
    mat = generate_wheel_matrix()
    print(mat)
    print(vertices_from_matrix(mat))
    #print(vertices_from_matrix(mat))
    #wheel = Wheel(1, 0.5, 0.1, vertices_from_matrix(mat))
