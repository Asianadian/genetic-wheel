import pygame
import pymunk
import pymunk.pygame_util
import pygame
import sys
import represention as rep
from pymunk.vec2d import Vec2d

# Initialize pygame and pymunk
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pymunk Falling Rectangle (Polygon)")

# Create a pymunk space
space = pymunk.Space()
space.gravity = (0, 900)  # Gravity pulling down

# Create a static floor
floor = pymunk.Segment(space.static_body, (0, HEIGHT-50), (WIDTH, HEIGHT-50), 5)
floor.elasticity = 0.1  # Make the floor bouncy
floor.friction = 0.8
space.add(floor)

# Create a falling rectangle using pymunk.Poly (polygon)
mass = 1
vertices = rep.get_coordinates(rep.init_representation())
moment = pymunk.moment_for_poly(mass, vertices)
body = pymunk.Body(mass, moment)
body.position = (300, 100)  # Start above the floor
shape = pymunk.Poly(body, vertices)
shape.elasticity = 0.1  # Make the rectangle bouncy
shape.friction = 0.5
space.add(body, shape)

# Pygame clock for frame rate control
clock = pygame.time.Clock()

# Set up the pymunk drawing utilities
draw_options = pymunk.pygame_util.DrawOptions(screen)

# polygon for wheel
coord = rep.get_coordinates(rep.init_representation())

# print(coord)

# Create a circular body
# mass = 5
# radius = 30
# moment = pymunk.moment_for_circle(mass, 0, radius)
# circle_body = pymunk.Body(mass, moment)
# circle_body.position = 200, 100  # Starting position
# circle_shape = pymunk.Circle(circle_body, radius)
# circle_shape.friction = 0.5  # Friction for rolling
# space.add(circle_body, circle_shape)

# Create ground
# ground = pymunk.Segment(space.static_body, (0, 550), (800, 550), 5)
# ground.friction = 1.0
# space.add(ground)

# Apply a tangential force to the circle
# force = (5000, 0)  # Force vector to the right
# point = (radius, 0)  # Point on the right edge of the circle
# circle_body.apply_impulse_at_local_point(force, point)

start_ticks = pygame.time.get_ticks()

# Simulation loop
while ((pygame.time.get_ticks()-start_ticks)/1000) < 4:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    print(shape.body.position)

    shape.body.torque = 20000

    # Step the physics simulation
    space.step(1 / 60.0)

    # Fill the screen with white
    screen.fill((255, 255, 255))

    # Draw the pymunk space (including the floor and the rectangle)
    space.debug_draw(draw_options)

    # Update the display
    pygame.display.flip()
    clock.tick(50)

# Clean up pygame
pygame.quit()
