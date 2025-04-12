import pygame, sys, random
from pygame.math import Vector2
from stuff import *

pygame.init()

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, very_light_red, block_rect)
        self.can_turn = True
            

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy
        
    def add_block(self):
        self.new_block = True
        
class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        pygame.draw.rect(screen, soft_green, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
        self.can_turn = True

    def draw_elements(self):
        self.snake.draw_snake()
        self.fruit.draw_fruit()

    def check_collision(self):
        if self.snake.body[0] == self.fruit.pos:
            self.fruit.randomize()
            self.snake.add_block()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
            
    def game_over(self):
        print("Game Over")
        pygame.quit()
        sys.exit()

screen = pygame.display.set_mode((Screen_W, Screen_H))
pygame.display.set_caption("Snake Game")

main = MAIN()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main.update()
        if event.type == pygame.KEYDOWN and main.can_turn == True:
            if event.key == pygame.K_UP and main.snake.direction != (0, 1):
                main.snake.direction = Vector2(0, -1)
                main.can_turn = False
            if event.key == pygame.K_DOWN and main.snake.direction != (0, -1):
                main.snake.direction = Vector2(0, 1)
                main.snake.can_turn = False
            if event.key == pygame.K_RIGHT and main.snake.direction != (-1, 0):
                main.snake.direction = Vector2(1, 0)
                main.snake.can_turn = False
            if event.key == pygame.K_LEFT and main.snake.direction != (1, 0):
                main.snake.direction = Vector2(-1, 0)
                main.can_turn = False

    screen.fill(light_green)
    main.draw_elements()

    pygame.display.update()
    clock.tick(60)


    
