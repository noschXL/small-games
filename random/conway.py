import pygame
import time
from sys import exit


pygame.init()
width, height = 1000, 1000
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

maps = [[[False] * round(width / 10) for _ in range(round(height / 10))],
        [[False] * round(width / 10) for _ in range(round(height / 10))]
       ]

pygame.key.set_repeat(500, 25)

start = False
lastm = 0
lastk = 0

def draw(gamemap):
    for x in range(len(gamemap)):
        for y in range(len(gamemap)):
            if gamemap[x][y]:
                pygame.draw.rect(screen, "#FFFFFF", (x * 10, y * 10, 10, 10))
            else:
                pygame.draw.rect(screen, "#A0A0A0", (x * 10, y * 10, 10, 10), 1)
            
def update(newmap, gamemap):
    directions = [(-1,-1), (-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1)]
    maxwidth =  round(width / 10) - 1
    for x in range(len(gamemap)):
        for y in range(len(gamemap)):
            neighbours = 0
            for direction in directions:
                newpos = [x + direction[0], y + direction[1]]
                if x + direction[0] > maxwidth:
                    newpos[0] = 0
                if y + direction[1] > maxwidth:
                    newpos[1] = 0

                if gamemap[newpos[0]][newpos[1]]:
                    neighbours += 1

            if gamemap[x][y]:
                newmap[x][y] = neighbours == 2 or neighbours == 3
            else:
                newmap[x][y] = neighbours == 3

i = 0
FPS = 120
speed = 12

currtime = time.time()

time.sleep(1 / FPS)

while True:
    
    dt = time.time() - currtime
    currtime = time.time()
    if i % round(FPS / 4) == 0:
        print(round(1 / dt))
    i += 1
    i %= FPS

    screen.fill("#000000")
    mousepress = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if lastk == 0:
            start = not start
            lastk = 1
    else:
        lastk = 0
    if keys[pygame.K_RIGHT]:
        speed -= 1
    if keys[pygame.K_LEFT]:
        speed += 1

    speed = max(speed, 0)
    speed = min(speed, FPS - 1)

    if pygame.mouse.get_pressed()[0]:
        if lastm == 0:
            mousepress = True
        lastm = 1
    else:
        lastm = 0

    if mousepress:
        xy = pygame.mouse.get_pos()
        x = xy[0] // 10
        y = xy[1] // 10
        maps[1][x][y] = not maps[1][x][y]

    if start:
        update(maps[1], maps[0])
        maps.reverse()
    draw(maps[1])
    pygame.display.update()


    clock.tick(round(FPS - speed))