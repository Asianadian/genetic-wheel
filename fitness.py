import pygame
import pymunk
import pymunk.pygame_util
import pygame
import represention as rep
from pymunk.vec2d import Vec2d

WIDTH, HEIGHT = 600, 400

def generate_space():
    space = pymunk.Space()
    space.gravity = (0, 900)

    floor = pymunk.Segment(space.static_body, (0, HEIGHT-50), (2000, HEIGHT-50), 5)
    floor.elasticity = 0.1
    floor.friction = 0.8
    space.add(floor)

    return space

def fitness_distance_visualize(representation):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pymunk Falling Rectangle (Polygon)")

    space = generate_space()

    mass = 1
    position = (50, HEIGHT-100)
    elasticity = 0.1
    friction = 0.5
    wheel = rep.Wheel(mass, friction, elasticity, representation, position)
    space.add(wheel.body, wheel.shape)

    clock = pygame.time.Clock()

    draw_options = pymunk.pygame_util.DrawOptions(screen)

    t = 0

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

    return wheel.body.position[0]

def fitness_distance(representation):
    space = generate_space()

    mass = 1
    position = (50, HEIGHT-100)
    elasticity = 0.1
    friction = 0.5
    try:
        wheel = rep.Wheel(mass, friction, elasticity, representation, position)
    except Exception as e:
        return 1e-10
    
    space.add(wheel.body, wheel.shape)

    t = 0
  
    while t < 600:
        wheel.body.torque = 10000

        space.step(1 / 60.0)
        t += 1
        
    return wheel.body.position[0]

if __name__ == '__main__':
  rand = rep.generate_wheel_matrix()
  print(fitness_distance_visualize(rand))
  print(fitness_distance(rand))