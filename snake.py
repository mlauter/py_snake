import pygame

black = 0, 0, 0
green = 0, 255, 0

class Head(object):

    def __init__(self,position,speed=[0,0],lastmove=0, delay=20):
        self.position = position
        self.square = pygame.Surface((15, 15))
        self.speed = speed
        self.lastmove = self.now = lastmove
        self.delay = delay

    def update(self):
        self.handle_keys(self.speed)
        if self.now > self.lastmove + self.delay:
            self.position[0] += self.speed[0]
            self.position[1] += self.speed[1]
            self.lastmove = self.now
        self.now += 1

    def draw(self,screen):
        self.square.fill(green)
        screen.fill(black)
        screen.blit(self.square,self.position)
        pygame.display.flip()

    def handle_keys(self,speed):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_LEFT] and speed != [15,0]:
            self.speed = [-15,0]
        elif keys_pressed[pygame.K_RIGHT] and speed != [-15,0]:
            self.speed = [15,0]
        elif keys_pressed[pygame.K_UP] and speed != [0,15]:
            self.speed = [0,-15]
        elif keys_pressed[pygame.K_DOWN] and speed != [0,-15]:
            self.speed = [0,15]    