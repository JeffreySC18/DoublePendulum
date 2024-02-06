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
    return math.sqrt((p2[1] - p1[1]) ** 2 + (p2[0] - p1[0]) ** 2)


def calculate_angle(p1, p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])


# Draw the simulation for me, anything I want to draw into the window will be done here, not the space, using pygame stuff
def draw(space, window, draw_options, line):
    window.fill("white")
    if line:
        pygame.draw.line(window, "black", line[0], line[1], 3)
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


def create_structure(space, width, height):
    BROWN = (139, 69, 19, 100)
    rect = [
        [(600, height-120), (40, 200), BROWN, 100],
        [(900, height - 120), (40, 200), BROWN, 100],
        [(750, height - 240), (340, 40), BROWN, 100]
    ]
    for pos, size, color, mass in rect:
        body = pymunk.Body()
        body.position = pos
        shape = pymunk.Poly.create_box(body, size, radius=1)
        shape.color = color
        shape.mass = mass
        shape.elasticity = 0.4
        shape.friction = .4
        space.add(body, shape)

#def create_double_double(space):
    #break
def create_swinging_ball(space):
    rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    rotation_center_body.position = (600,280)

    body = pymunk.Body()
    body.position = (600,280)
    line = pymunk.Segment(body, (0,0), (255,0), 5)
    circle = pymunk.Circle(body, 40, (255,0))
    line.friction = .1
    circle.friction = .1
    line.mass = 8
    circle.mass = 30
    circle.elasticity = .95
    rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0,0), (0,0))
    space.add(circle, line, body, rotation_center_joint)

# 0,0 is top left corner
def create_ball(space, radius, mass, pos):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.elasticity = .9
    shape.friction = .3
    shape.color = (255, 0, 0, 100)
    space.add(body, shape)
    return shape


def run(window, width, height):
    run = True
    clock = pygame.time.Clock()
    fps = 144
    dt = 1 / fps

    # Simulated space in pymunk
    space = pymunk.Space()
    space.gravity = (0, grav)

    pressed_pos = None
    ball = None

    create_boundary(space, width, height)
    create_structure(space, width, height)
    create_swinging_ball(space)
    #create_double_double(space)

    # PyMunk doesn't inherntly draw, so this is the machinery to draw stuff
    draw_options = pymunk.pygame_util.DrawOptions(window)
    while run:
        line = None
        if ball and pressed_pos:
            line = [pressed_pos, pygame.mouse.get_pos()]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not ball:
                    pressed_pos = pygame.mouse.get_pos()
                    ball = create_ball(space, 30, 10, pressed_pos)
                elif pressed_pos:
                    angle = calculate_angle(*line)
                    force = calculate_distance(*line) * 50
                    fx = math.cos(angle) * force
                    fy = math.sin(angle) * force
                    ball.body.body_type = pymunk.Body.DYNAMIC
                    ball.body.apply_impulse_at_local_point((fx, fy), (0, 0))
                    pressed_pos = None
                else:
                    space.remove(ball, ball.body)
                    ball = None

        draw(space, window, draw_options, line)
        space.step(dt)
        clock.tick(fps)


if __name__ == "__main__":
    run(window, Width, Height)
