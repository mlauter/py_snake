import sys, pygame, random

def random_grid_position(grid_square,max_size):
    return random.randint(0,max_size/grid_square)*grid_square

class Game(object):

    def __init__(self, width, height):
        self.size = width, height
        self.grid_square = 10
        self.screen = pygame.display.set_mode(self.size)
        self.bodies = [Head([width/2-self.grid_square/2,height/2-self.grid_square/2]),Food(self)]
        while 1:

            self.update()
            self.draw()

    def update(self):
        for body in self.bodies:
            body.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

    def draw(self):
        self.screen.fill((0,0,0))
        for body in self.bodies:
            body.draw(self.screen)
        pygame.display.flip()


class Head(object):

    def __init__(self,position, speed=[0,0],lastmove=0, delay=20):
        self.position = position
        self.square = pygame.Surface((10, 10))
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
        self.square.fill((0, 255, 0))
        screen.blit(self.square,self.position)

    def handle_keys(self,speed):
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_LEFT] and speed != [10,0]:
            self.speed = [-10,0]
        elif keys_pressed[pygame.K_RIGHT] and speed != [-10,0]:
            self.speed = [10,0]
        elif keys_pressed[pygame.K_UP] and speed != [0,10]:
            self.speed = [0,-10]
        elif keys_pressed[pygame.K_DOWN] and speed != [0,-10]:
            self.speed = [0,10]

class Food(object):
    def __init__(self,game):

        self.position = [random_grid_position(game.grid_square, game.size[0])-game.grid_square/2, random_grid_position(game.grid_square, game.size[1])-game.grid_square/2]
        self.square = pygame.Surface((10, 10))

    def update(self):
        pass

    def draw(self,screen):
        self.square.fill((0, 0, 255))
        screen.blit(self.square,self.position)

if __name__ == "__main__":
    pygame.init()
    Game(400,400)
