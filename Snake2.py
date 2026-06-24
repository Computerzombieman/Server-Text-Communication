import pygame
import random
import heapq

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Snake")

move_delay = 1

width = 600
height = 600
cell_size = 20

grid_width = width // cell_size
grid_height = height // cell_size

directions = [
    (1, 0),   # Right
    (0, 1),   # Down
    (-1, 0),  # Left
    (0, -1)   # Up
]
direction_index = 0

snake = [(5,5),(4,5),(3,5)]

ate_food = False

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def displayGraphics():
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

def a_star(start,goal,snake_body):
    open_set = []
    heapq.heappush(open_set, (0,start))

    came_from = {}
    g_score = {start : 0}

    snake_set = set(snake_body[:-1])

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            if not (0 <= neighbor[0] < grid_width and 0 <= neighbor[1] < grid_height):
                continue

            if neighbor in snake_set:
                continue
            
            tentative_g = g_score[current] + 1

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g

                f = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f, neighbor))

    return None

def eat_apple():
    global apple
    global ate_food

    ate_food = True
    
    apple = spawn_apple()

def snakeAlgorithm():
    global snake
    global apple
    global ate_food
    global direction_index

    a_result = a_star(snake[0],apple,snake[1:])
    if a_result:

        print(a_result)

        new_head = a_result[0]

        snake.insert(0,new_head)
        if not ate_food:
            snake.pop()
        else:
            ate_food = False
        if snake[0] == apple:
            eat_apple()

last_move_time = pygame.time.get_ticks()
running = True

while running:
    current_time = pygame.time.get_ticks()

    if current_time - last_move_time >= move_delay:
        snakeAlgorithm()
        last_move_time = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    displayGraphics()
    pygame.display.flip()
pygame.quit()