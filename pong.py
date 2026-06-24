import pygame

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong')

last_move_time = pygame.time.get_ticks()
running = True

x,y = (WIDTH/2,HEIGHT/2)
x_Speed,y_Speed = (100,-60)

P1 = HEIGHT/2-75

while running:
    current_time = pygame.time.get_ticks()
    screen.fill((0, 0, 0))
    
    pygame.draw.circle(screen,(255,255,255),(x,y),10)
    pygame.draw.rect(screen,(255,255,255),pygame.Rect(WIDTH-20, P1,10,150),0,3)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    x,y = (x+x_Speed/100,y+y_Speed/100)
    
    if y<P1+10:
        P1-=10
    if y>P1+140:
        P1+=10

    if x+7 >= WIDTH-20 and (y < P1+150 and y > P1):
        x_Speed*=-1
    if y+7 >= HEIGHT or y-7 <= 0:
        y_Speed*=-1

    if x-7 <= 0:
        x_Speed *=-1
    
    x_Speed+= x_Speed/10000
    y_Speed+=y_Speed/10000
    
    
    

    pygame.display.flip()


pygame.quit()