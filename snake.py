import sys, pygame, random, itertools

def random_grid_position(grid_square,max_size):
    return random.randint(grid_square,max_size/grid_square)*grid_square

class Game(object):

    def __init__(self, width, height):
        self.size = width, height
        self.grid_square = 10
        self.screen = pygame.display.set_mode(self.size)
        self.bodies = []
        self.bodies.append(Head([width/2-self.grid_square/2,height/2-self.grid_square/2],self))
        self.bodies.append(Food(self))

        while 1:

            self.update()
            self.draw()

    def add_body(self,body):
        self.bodies.append(body)

    def remove_body(self,body):
        self.bodies.remove(body)

    def detect_collision(self, body1, body2):
        if body1.position == body2.position:
            body1.collision(body2)
            body2.collision(body1)

    def detect_wall_collision(self, body):
        mins = [self.grid_square]*2
        maxs = [a - 2*b for a,b in zip(self.size, mins)] 
        if body.position[0] <= mins[0] or body.position[1] <= mins[1] or body.position[0] >= maxs[0] or body.position[1] >= maxs[1]:
            body.collision()

    def update(self):
        for pair in itertools.combinations(self.bodies,2):
            self.detect_collision(*pair)
        for body in self.bodies:
            if type(body) is Head:
                self.detect_wall_collision(body)
            body.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

    def draw(self):
        self.screen.fill((0,0,0))
        pygame.draw.rect(self.screen, (50,50,50), self.screen.get_rect(), 10)
        for body in self.bodies:
            body.draw(self.screen)
        pygame.display.flip()



class Head(object):
#make sure to tell any segment behind you what to do (take your old place)
    def __init__(self,position, game, speed=[0,0],lastmove=0, delay=10):
        self.position = position
        self.square = pygame.Surface((10, 10))
        self.speed = speed
        self.lastmove = self.now = lastmove
        self.delay = delay
        self.game = game
        self.segments = []
        for i in range(1,7):
            pos = [self.position[0], self.position[1]+i*self.game.grid_square]
            segment = Segment(self.game,pos)
            self.segments.append(segment)
            self.game.add_body(segment)

    def update(self):
        self.handle_keys(self.speed)
        if self.now > self.lastmove + self.delay:
            last_position = self.position[:]
            self.position[0] += self.speed[0]
            self.position[1] += self.speed[1]
            self.lastmove = self.now
            if self.speed != [0,0]:
                for segment in self.segments:
                    segment_last_position = segment.get_position()
                    if segment_last_position == self.position:
                        self.die()
                    else:
                        segment.move(last_position)
                        last_position = segment_last_position

        self.now += 1

    def collision(self,*args):
        if len(args) == 0:
            #wall collision
            self.die()
        else:
            #collision of head with food or self
            body2 = args[0]
            if type(body2) is Food:
                self.eat(body2)
            elif type(body2) is Segment:
                self.die()

    def eat(self,food):
        self.game.remove_body(food)
    #     foods = [body for body in self.game.bodies if type(body) is Food]
    #     for food in foods:
    #         if self.position == food.position:
    #             food.be_eaten()
    def die(self):
        for body in self.game.bodies:
            body.speed =[0,0]
        print "you died"

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

# make a segment class, instantiate five or so, make sure they follow the head around, each segment tells the one behind it what to do
class Segment(object):
    def __init__(self,game,position):
        self.position = position
        self.square = pygame.Surface((10, 10))
        self.game = game

    def update(self):
        pass

    def collision(self,body2):
        pass

    def get_position(self):
        return self.position

    #don't do this here
    def move(self,head_pos):
        self.position = head_pos

    def draw(self,screen):
        self.square.fill((0, 255, 0))
        screen.blit(self.square,self.position)

        
class Food(object):
    def __init__(self,game):
        #this is rather ugly
        self.position = [random_grid_position(game.grid_square, game.size[0])-game.grid_square/2, random_grid_position(game.grid_square, game.size[1])-game.grid_square/2]
        self.square = pygame.Surface((10, 10))
        self.game = game

    def update(self):
        pass

    def collision(self,body2):
        self.game.add_body(Food(self.game))

    def draw(self,screen):
        self.square.fill((0, 0, 255))
        screen.blit(self.square,self.position)

if __name__ == "__main__":
    pygame.init()
    Game(400,400)
