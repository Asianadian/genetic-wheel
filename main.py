import pymunk
import pymunk.pygame_util
import pygame
import sys
import represention as rep

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Create Pymunk space
space = pymunk.Space()
space.gravity = (0, 900)  # Gravity pointing downward

# polygon for wheel
coord = rep.get_coordinates(rep.init_representation())

# Create a dynamic body
body = pymunk.Body(1, pymunk.moment_for_poly(1, coord))
body.position = 300, 300

# Create a polygon shape (triangle)
shape = pymunk.Poly(body, coord)
space.add(body, shape)

# print(coord)

# Create a circular body
mass = 5
radius = 30
moment = pymunk.moment_for_circle(mass, 0, radius)
circle_body = pymunk.Body(mass, moment)
circle_body.position = 200, 100  # Starting position
circle_shape = pymunk.Circle(circle_body, radius)
circle_shape.friction = 0.5  # Friction for rolling
space.add(circle_body, circle_shape)

# Create ground
ground = pymunk.Segment(space.static_body, (0, 550), (800, 550), 5)
ground.friction = 1.0
space.add(ground)

# Apply a tangential force to the circle
force = (5000, 0)  # Force vector to the right
point = (radius, 0)  # Point on the right edge of the circle
circle_body.apply_impulse_at_local_point(force, point)

start_ticks = pygame.time.get_ticks()

# Simulation loop
while ((pygame.time.get_ticks()-start_ticks)/1000) < 10:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Clear screen
    screen.fill((255, 255, 255))
    space.step(1 / 50.0)  # Step simulation
    space.debug_draw(draw_options)
    pygame.display.flip()
    clock.tick(50)
