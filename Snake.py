import pygame
import random

pygame.init()

screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Hello Pygame")

move_delay = 50

width = 600
height = 600
cell_size = 40

grid_width = width // cell_size
grid_height = height // cell_size

snake = [(5,5),(4,5),(3,5)]

directions = [
    (1, 0),   # Right
    (0, 1),   # Down
    (-1, 0),  # Left
    (0, -1)   # Up
]

direction_index = 0



ate_food = False


def next_position(direction):
    head_x, head_y = snake[0]

    dx, dy = directions[direction]

    return (
        head_x + dx,
        head_y + dy
    )

def would_hit_body(direction):
    return next_position(direction) in snake

def can_escape(direction):
    pos = next_position(direction)

    safe_moves = 0

    for d in range(4):
        dx, dy = directions[d]

        check = (
            pos[0] + dx,
            pos[1] + dy
        )

        if check not in snake:
            safe_moves += 1

    return safe_moves > 1

def spawn_apple():
    attempts = 0

    while True:
        attempts += 1

        apple = (
            random.randint(0, grid_width - 1),
            random.randint(0, grid_height - 1)
        )

        if apple not in snake:
            return apple

apple = spawn_apple()

def turn_left():
    global direction_index
    if not would_hit_body((direction_index - 1) % 4):
        direction_index = (direction_index - 1) % 4

def turn_right():
    global direction_index
    if not would_hit_body((direction_index + 1) % 4):
        direction_index = (direction_index + 1) % 4

def eat_apple():
    global apple
    global ate_food

    ate_food = True
    
    apple = spawn_apple()
    print("Apple spawned at:", apple)


def move_snake():
    global snake
    global ate_food

    head_x, head_y = snake[0]
    dx, dy = directions[direction_index]
    new_head = ()
    if not would_hit_body(direction_index):
        new_head = (
        head_x + dx,
        head_y + dy
        )
    elif not would_hit_body((direction_index - 1) % 4):
        turn_left()
        dx, dy = directions[direction_index]
        new_head = (
        head_x + dx,
        head_y + dy
        )
    elif not would_hit_body((direction_index + 1) % 4):
        turn_right()
        dx, dy = directions[direction_index]
        new_head = (
        head_x + dx,
        head_y + dy
        )
    else:
        print("Game over!")

    if not new_head:
        return
    
    snake.insert(0, new_head)
    if not ate_food:
        snake.pop()
    else:
        ate_food = False

def snake_algorithm():
    global snake
    global apple
    global direction_index

    head_x, head_y = snake[0]
    apple_x, apple_y = apple

    desired_direction = None

    if apple_x < head_x:
        desired_direction = 2  # Left
    elif apple_x > head_x:
        desired_direction = 0  # Right
    elif apple_y < head_y:
        desired_direction = 3  # Up
    else:
        desired_direction = 1  # Down

    left_dir = (direction_index - 1) % 4
    right_dir = (direction_index + 1) % 4
    behind_dir = (direction_index + 2) % 4

    if left_dir == desired_direction:
        turn_left()

    elif right_dir == desired_direction:
        turn_right()

    elif desired_direction == behind_dir:
        turn_left()

last_move_time = pygame.time.get_ticks()
running = True

while running:
    current_time = pygame.time.get_ticks()
    
    if current_time - last_move_time >= move_delay:
        snake_algorithm()
        move_snake()
        last_move_time = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    for x in range(0, width, cell_size):
        pygame.draw.line(screen, (50, 50, 50), (x, 0), (x, height))

    for y in range(0, height, cell_size):
        pygame.draw.line(screen, (50, 50, 50), (0, y), (width, y))

    for x, y in snake:
        pygame.draw.rect(
            screen,
            (0, 255, 0),
            (x * cell_size, y * cell_size, cell_size, cell_size)
        )
    
    pygame.draw.rect(
    screen,
    (255, 0, 0),
    (
        apple[0] * cell_size,
        apple[1] * cell_size,
        cell_size,
        cell_size
    )
    )

    if snake[0] == apple:
        eat_apple()
        

    pygame.display.flip()

pygame.quit()