import pymunk
import pygame
import pymunk.pygame_util
import math

pygame.init()
Width, Height = 1200, 900
window = pygame.display.set_mode((Width, Height))
# In pygame for some reason as you go down the y goes up :(
grav = 981

def calculate_distance(p1, p2):
    return math.sqrt((p2[1] - p1[1]) ** 2 + (p2[0]-p1[0])**2)

def calculate_angle(p1, p2):
    return math.atan2(p2[1] - p1[1], p2[0]-p1[0])
# Draw the simulation for me, anything I want to draw into the window will be done here, not the space, using pygame stuff
def draw(space, window, draw_options):
    window.fill("white")
    space.debug_draw(draw_options)
    pygame.display.update()


# Creating rect(width and height of center, width, height
def create_boundary(space, width, height):
    rects = [
        [(width / 2, height - 10), (width, 20)],
        [(width / 2, 10), (width, 20)],
        [(10, height / 2), (20, height)],
        [(width - 10, height / 2), (20, height)]
    ]

    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = .4
        shape.friction = .5
        space.add(body, shape)


# 0,0 is top left corner
def create_ball(space, radius, mass):
    body = pymunk.Body()
    body.position = (300, 300)
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.elasticity = .9
    shape.friction = .4
    shape.color = (255, 0, 0, 100)
    space.add(body, shape)
    return shape


def run(window, width, height):
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1 / fps

    # Simulated space in pymunk
    space = pymunk.Space()
    space.gravity = (0, grav)

    ball = create_ball(space, 30, 10)

    create_boundary(space, width, height)

    # PyMunk doesn't inherntly draw, so this is the machinery to draw stuff
    draw_options = pymunk.pygame_util.DrawOptions(window)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                ball.body.apply_impulse_at_local_point((30000, 0), (0,0))
        draw(space, window, draw_options)
        space.step(dt)
        clock.tick(fps)


if __name__ == "__main__":
    run(window, Width, Height)
