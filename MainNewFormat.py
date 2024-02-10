import pymunk
import pygame
import pymunk.pygame_util
import math

pygame.init()

display = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
space = pymunk.Space()
fps = 144
dt = 1 / fps


def convertCord(point):
    return int(point[0]), int(600 - point[1])


class Ball():
    def __init__(self, x, y):
        self.body = pymunk.Body()
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, 10)
        self.shape.density = 1
        self.shape.elasticity = 1

    def draw(self):
        pygame.draw.circle(display, (255, 0, 0), convertCord(self.body.position), 10)


def game():
    ball1 = Ball(300, 300)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        display.fill((255, 255, 255))
        ball1.draw()
        pygame.display.update()
        clock.tick(fps)
        space.step(dt)


game()
pygame.quit()
