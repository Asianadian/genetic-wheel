import numpy as np
import pygame
import pygame
import pymunk
import pymunk.pygame_util
import represention as rep
from const import WIDTH, HEIGHT
import sys

'''
Exception handling for Chipmunk2D 

pymunk terminates the program instead of throwing exceptions in some cases
'''
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    print(f"Uncaught exception: {exc_value}")
    raise Exception("System exception")
sys.excepthook = handle_exception

def fitness_from_distance(distance):
    return max(1e-10, distance)

'''
Creates simulation space

pymunk Space and horizontal Segment with set physical properties

Returns pymunk Space
'''
def generate_space():
    space = pymunk.Space()
    space.gravity = (0, 981)

    floor = pymunk.Segment(space.static_body, (0, HEIGHT-50), (100000, HEIGHT-50), 5)
    floor.filter = pymunk.ShapeFilter(group=1)
    floor.elasticity = 0.0
    floor.friction = 0.8
    space.add(floor)

    return space

'''
Visualizes list of wheels in pygame
'''
def visualize(representations, meta_data=''):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption(f"Rolling Wheel {meta_data}")

    draw_options = pymunk.pygame_util.DrawOptions(screen)
    draw_options.shape_outline_color = (10, 20, 30, 40)
    draw_options.flags = pymunk.SpaceDebugDrawOptions.DRAW_SHAPES | pymunk.SpaceDebugDrawOptions.DRAW_CONSTRAINTS

    space = generate_space()

    wheels = []

    for i, representation in enumerate(representations):
        wheel = try_creating_wheel(representation)
        if wheel:
            wheels.append(wheel)
            wheel.shape.color = (255*i/len(representations), 255*i/len(representations), 255*i/len(representations), 32)
            space.add(wheel.body, wheel.shape)

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

            screen.fill((20, 205, 240))

            space.debug_draw(draw_options)

            pygame.display.flip()
            clock.tick(60)
        
        pygame.display.quit()
        pygame.quit()
    except:
        pygame.display.quit()
        pygame.quit()
        print("Failed visualization")
    
'''
Visualizes 1 wheel in pygame

Returns distance traveled by wheel
'''
def fitness_distance_visualize(representation):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Rolling Wheel")
    
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    space = generate_space()

    wheel = try_creating_wheel(representation)

    if not wheel:
        return fitness_from_distance(1e-10)
    
    space.add(wheel.body, wheel.shape)

    clock = pygame.time.Clock()

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
        
        pygame.display.quit()
        pygame.quit()
        return fitness_from_distance(wheel.body.position[0])
    except Exception as e:
        pygame.display.quit()
        pygame.quit()
        return fitness_from_distance(1e-10)

'''
Simulates 1 wheel in pygame

Returns distance traveled by wheel
'''
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
        
        pygame.display.quit()
        pygame.quit()
        return fitness_from_distance(wheel.body.position[0])
    except Exception as e:
        pygame.display.quit()
        pygame.quit()
        return fitness_from_distance(1e-10)
    
'''
???
'''
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

'''
Handles failed wheels

Returns wheel object if possible
'''  
def try_creating_wheel(representation):
    try:
        return rep.wheel_from_raw_data(representation, (50, HEIGHT-150))
    except Exception as e:
        return None