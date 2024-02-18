import pymunk
import pygame
import pymunk.pygame_util
import math

pygame.init()

display = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0, -981)
fps = 144
dt = 1 / fps


def convertCord(point):
    return int(point[0]), int(600 - point[1])


class Ball:
    def __init__(self, x, y):
        self.body = pymunk.Body()
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, 10)
        self.shape.density = 1
        self.shape.elasticity = 1
        space.add(self.body, self.shape)

    def draw(self):
        pygame.draw.circle(display, (255, 0, 0), convertCord(self.body.position), 10)


class String:
    def __init__(self, body1, attachment, identifier="body"):
        self.body1 = body1
        if identifier == "body":
            self.body2 = attachment

        elif identifier == "position":
            self.body2 = pymunk.Body(body_type=pymunk.Body.STATIC)
            self.body2.position = attachment
        joint = pymunk.PinJoint(self.body1, self.body2)
        space.add(joint)

    def draw(self):
        pos1 = convertCord(self.body1.position)
        pos2 = convertCord(self.body2.position)
        pygame.draw.line(display, (0, 0, 0), pos1, pos2, 2)


def game():
    ball1 = Ball(200, 450)
    ball2 = Ball(100, 150)

    string1 = String(ball1.body, (300, 550), identifier="position")
    string2 = String(ball1.body, ball2.body)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        display.fill((255, 255, 255))
        ball1.draw()
        ball2.draw()
        string1.draw()
        string2.draw()
        pygame.display.update()
        clock.tick(fps)
        space.step(dt)


game()
pygame.quit()
