import pymunk
import pygame
import pymunk.pygame_util
import math

pygame.init()
Width, Height = 1200, 900
window = pygame.display.set_mode((Width, Height))
# In pygame for some reason as you go down the y goes up :(
grav = 981

#Draw the simulation for me, anything I want to draw into the window will be done here, not the space, using pygame stuff
def draw(space, window, draw_options):
    window.fill("white")
    space.debug_draw(draw_options)
    pygame.display.update()

def run(window, width, height):
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1/fps

    #Simulated space in pymunk
    space = pymunk.Space()
    space.gravity = (0, grav)

    #PyMunk doesn't inherntly draw, so this is the machinery to draw stuff
    draw_options = pymunk.pygame_util.DrawOptions(window)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        draw(space, window, draw_options)
        space.step(dt)
        clock.tick(fps)


if __name__ == "__main__":
    run(window, Width, Height)
