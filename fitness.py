import pygame
import pymunk
import pymunk.pygame_util
import pygame
import represention as rep
from const import WIDTH, HEIGHT
from pymunk.vec2d import Vec2d
import numpy as np
import sys

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        # Allow KeyboardInterrupt to exit the program
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    print(f"Uncaught exception: {exc_value}")
    raise Exception("sys except")

sys.excepthook = handle_exception

# bad distance -> 1
# good distance -> inf
def fitness_from_distance(distance):
    return max(1e-10, distance)

    # sigmoid = 1/(1+np.exp(-distance))
    # return 1/(1-sigmoid)

def generate_space():
    space = pymunk.Space()
    space.gravity = (0, 900)

    floor = pymunk.Segment(space.static_body, (0, HEIGHT-50), (100000, HEIGHT-50), 5)
    floor.filter = pymunk.ShapeFilter(group=1)
    floor.elasticity = 0.0
    floor.friction = 0.8
    space.add(floor)

    return space

def visualize(representations):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    pygame.display.set_caption("Rolling Wheel")

    draw_options = pymunk.pygame_util.DrawOptions(screen)
    draw_options.shape_outline_color = (0, 0, 0, 255)

    space = generate_space()

    wheels = []

    for i, representation in enumerate(representations):
        wheel = try_creating_wheel(representation)
        if wheel:
            #print(representation)
            wheels.append(wheel)
            space.add(wheel.body, wheel.shape)
            wheel.shape.color = (255*np.random.rand(), 255*np.random.rand(), 255*np.random.rand(), 32)

    clock = pygame.time.Clock()

    t = 0
    try:
        while t < 600:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            for wheel in wheels:
                wheel.body.torque = 10000

            space.step(1 / 60.0)
            t += 1

            screen.fill((255, 255, 255))

            space.debug_draw(draw_options)

            pygame.display.flip()
            clock.tick(60)
    except:
        print("Failed visualization")

def fitness_distance_visualize(representation):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Rolling Wheel")

    space = generate_space()

    wheel = try_creating_wheel(representation)
    if not wheel:
        return fitness_from_distance(1e-10)
    
    space.add(wheel.body, wheel.shape)

    clock = pygame.time.Clock()
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    t = 0
    try:
        while t < 600:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            wheel.body.torque = 10000

            space.step(1 / 60.0)
            t += 1

            screen.fill((255, 255, 255))

            space.debug_draw(draw_options)

            pygame.display.flip()
            clock.tick(60)

        return fitness_from_distance(wheel.body.position[0])
    except Exception as e:
        return fitness_from_distance(1e-10)

def fitness_distance(representation):
    space = generate_space()

    wheel = try_creating_wheel(representation)
    if not wheel:
        return fitness_from_distance(1e-10)
    
    space.add(wheel.body, wheel.shape)

    t = 0
    try:
        while t < 600:
            wheel.body.torque = 10000

            space.step(1 / 60.0)
            t += 1
            
        return fitness_from_distance(wheel.body.position[0])
    except Exception as e:
        return fitness_from_distance(1e-10)
    
def draw_wheel_polygon(representation):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Static Wheel")

    space = pymunk.Space()
    space.gravity = (0, 0)

    wheel = try_creating_wheel(representation)
    
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    screen.fill((255, 255, 255))
    space.debug_draw(draw_options)
    pygame.display.flip()
      
def try_creating_wheel(representation):
    try:
        return rep.wheel_from_raw_data(representation, (50, HEIGHT-150))
    except Exception as e:
        return None

if __name__ == '__main__':
  rand = rep.generate_wheel_matrix()
  print(fitness_distance_visualize(rand))
  print(fitness_distance(rand))