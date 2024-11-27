import pygame
import pymunk
import pymunk.pygame_util
import pygame
import represention as rep
from pymunk.vec2d import Vec2d

def fitness_distance_visualize(representation):
    # Initialize pygame and pymunk
    pygame.init()

    # Set up the screen
    WIDTH, HEIGHT = 600, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pymunk Falling Rectangle (Polygon)")

    # Create a pymunk space
    space = pymunk.Space()
    space.gravity = (0, 900)

    # Create a static floor
    floor = pymunk.Segment(space.static_body, (0, HEIGHT-50), (2000, HEIGHT-50), 5)
    floor.elasticity = 0.1
    floor.friction = 0.8
    space.add(floor)

    # Create a falling rectangle using pymunk.Poly (polygon)
    mass = 1
    vertices = rep.get_coordinates(representation)
    moment = pymunk.moment_for_poly(mass, vertices)
    body = pymunk.Body(mass, moment)
    body.position = (300, 100)
    shape = pymunk.Poly(body, vertices)
    shape.elasticity = 0.1
    shape.friction = 0.5
    space.add(body, shape)

    # Pygame clock for frame rate control
    clock = pygame.time.Clock()

    # Set up the pymunk drawing utilities
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    t = 0

    while t < 600:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        shape.body.torque = 20000

        space.step(1 / 60.0)
        t += 1

        # Fill the screen with white
        screen.fill((255, 255, 255))

        # Draw the pymunk space (including the floor and the rectangle)
        space.debug_draw(draw_options)

        # Update the display
        pygame.display.flip()
        clock.tick(60)

    return body.position[0]

def fitness_distance(representation):
    WIDTH, HEIGHT = 600, 400

    # Create a pymunk space
    space = pymunk.Space()
    space.gravity = (0, 900)

    # Create a static floor
    floor = pymunk.Segment(space.static_body, (0, HEIGHT-50), (2000, HEIGHT-50), 5)
    floor.elasticity = 0.1
    floor.friction = 0.8
    space.add(floor)

    # Create a falling rectangle using pymunk.Poly (polygon)
    mass = 1
    vertices = rep.get_coordinates(representation)
    moment = pymunk.moment_for_poly(mass, vertices)
    body = pymunk.Body(mass, moment)
    body.position = (300, 100)
    shape = pymunk.Poly(body, vertices)
    shape.elasticity = 0.1
    shape.friction = 0.5
    space.add(body, shape)

    t = 0

    while t < 600:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        shape.body.torque = 20000

        space.step(1 / 60.0)
        t += 1
        
    return body.position[0]

random_wheel = rep.init_representation()
print(fitness_distance_visualize(random_wheel))
print(fitness_distance(random_wheel))