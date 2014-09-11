import sys, pygame, random, itertools, time

class Game(object):

    def __init__(self, screen):
        self.screen = screen
        self.size = screen.get_size()
        self.grid_square = 10
        self.keys_pressed = []
        self.set_start_state()
        
    def set_start_state(self):
        width, height = self.size
        self.screen_center = [width / 2, height / 2]
        self.snake = Snake(self.screen_center)
        self.food = Food(self.new_food_position())

    def run(self):
        last_move_time = time.time()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
            
            self.set_keys()

            now = time.time()
            if now >= last_move_time + .18:
                last_move_time = now
                self.update()
                if self.snake_out_of_bounds() or self.snake.self_collision():
                    break
                self.draw()

    def set_keys(self):
        keys_pressed = pygame.key.get_pressed()
        if sum(keys_pressed) != 0:
            self.keys_pressed = keys_pressed

    def update(self):
        food_collision = self.food.position == self.snake.positions[0]
        if food_collision:
            self.food.position = self.new_food_position()
        self.snake.update(self.get_speed_delta(), food_collision)

    def get_speed_delta(self):
        if self.keys_pressed[pygame.K_LEFT]:
            return [-self.grid_square, 0]
        elif self.keys_pressed[pygame.K_RIGHT]:
            return [self.grid_square, 0]
        elif self.keys_pressed[pygame.K_UP]:
            return [0, -self.grid_square]
        elif self.keys_pressed[pygame.K_DOWN]:
            return [0, self.grid_square]
        else:
            return [0, 0]

    def new_food_position(self):
        x = self.random_valid_coordinate(0)
        y = self.random_valid_coordinate(1)
        for position in self.snake.positions:
            if [x, y] == position:
                return self.new_food_position()
        return [x, y]

    def random_valid_coordinate(self, axis):
        num_squares = self.size[axis] / self.grid_square - 1
        return random.randint(0, num_squares) * self.grid_square

    def snake_out_of_bounds(self):
        head_posx, head_posy = self.snake.positions[0]
        return head_posx < 0 or head_posx > self.size[0] - self.grid_square or\
               head_posy < 0 or head_posy > self.size[1] - self.grid_square

    def draw(self):
        self.screen.fill((0,0,0))
        self.food.draw(self.screen)
        self.snake.draw(self.screen)
        pygame.display.flip()

class Snake(object):
    def __init__(self, position, speed=[0,0]):
        self.positions = [position]
        self.speed = speed

    def update(self, speed_delta, food_collision=False):
        self.set_speed(speed_delta)
        head_pos = self.new_head_position()

        self.positions.insert(0, head_pos)
        if not food_collision:
            self.positions.pop()

    def new_head_position(self):
        current_head = self.positions[0]
        return [current_head[0] + self.speed[0], 
                current_head[1] + self.speed[1]]

    def set_speed(self, speed_delta):
        if speed_delta == [0, 0]:
            pass
        elif self.speed == [0, 0]:
            self.speed = speed_delta
        # change speed only if speed_delta is orthogonal to speed
        elif abs(self.speed[0]) != abs(speed_delta[0]):
            self.speed = speed_delta

    def self_collision(self):
        head_pos = self.positions[0]
        for position in self.positions[1:]:
            if position == head_pos:
                return True
        return False

    def draw(self, screen):
        square = pygame.Surface((10, 10))
        square.fill((0, 255, 0))
        for position in self.positions:
            screen.blit(square, position)
        
class Food(object):
    def __init__(self, position):
        self.square = pygame.Surface((10, 10))
        self.position = position

    def draw(self,screen):
        self.square.fill((0, 0, 255))
        screen.blit(self.square,self.position)

class GameMenu(object):
    def __init__(self, screen, items, bg_color=(0, 0, 0), font_size=30, font_color=(255, 255, 255)):
        
        self.screen = screen
        self.scr_width = screen.get_rect().width
        self.scr_height = screen.get_rect().height
        self.bg_color = bg_color
        self.font = pygame.font.Font('ARCADECLASSIC.TTF', 26)
        self.font_color = font_color
        self.items = []

        for index, item in enumerate(items):
            label = self.font.render(item, 1, font_color)
 
            width = label.get_rect().width
            height = label.get_rect().height
 
            posx = (self.scr_width / 2) - (width / 2)
            t_h = len(items) * height
            posy = (self.scr_height / 2) - (t_h / 2) + (index * height)
 
            self.items.append([item, label, (width, height), (posx, posy)])

    def run(self):
        mainloop = True
        while mainloop:
 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        mainloop = False
                    elif event.key==pygame.K_q:
                        mainloop = False
                        sys.exit()
            # Redraw the background
            self.screen.fill(self.bg_color)
            for name, label, (width, height), (posx, posy) in self.items:
                self.screen.blit(label, (posx, posy))
            pygame.display.flip()

def runner():
    screen = pygame.display.set_mode((300, 300))
    
    start_menu_items = ['Welcome to Snake',
                        'Press ENTER to play', 
                        'Press Q to quit']
    end_menu_items = ['You died',
                      'Press ENTER to try again', 
                      'Press Q to quit'];

    start_menu = GameMenu(screen, start_menu_items)
    end_menu = GameMenu(screen, end_menu_items)
    game = Game(screen)

    while True:
        start_menu.run()
        game.run()
        game.set_start_state()
        end_menu.run()
            

if __name__ == "__main__":
    pygame.init()
    runner()
