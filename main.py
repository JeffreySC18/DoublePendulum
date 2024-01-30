import pymunk
import pygame
import pymunk.pygame_util
import math

pygame.init()
Width, Height = 1200, 900
window = pygame.display.set_mode((Width, Height))
#In pygame for some reason as you go down the y goes up :(
grav = 981


def run(window, width, height):
    run = True
    clock = pygame.time.Clock()
    fps = 60

    space = pymunk.Space()
    space.gravity = (0, grav)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        clock.tick(fps)

if __name__ == "__main__":
    run(window, Width, Height)
