import sys, pygame
from pygame import *
from snake import *
pygame.init()

size = width, height = 400, 350
speed = [4,4]
black = 0, 0, 0
green = 0, 255, 0

screen = pygame.display.set_mode(size)

bodies = [Head([width/2,height/2])]

# square = pygame.Surface((15, 15))
# squarerect = square.get_rect()

while 1:
    for body in bodies:
        body.update()
        body.draw(screen)
    for event in pygame.event.get():
        if event.type == QUIT: sys.exit()






    