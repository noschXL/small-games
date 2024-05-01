import pygame
import numpy
import random
import math
from sys import exit


width = 800
height = 800
pygame.init()
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

all_maps = []

def blur(Maps, map_height):
    NewMaps = Maps
    for x in range(map_height):
        for y in range(map_height):
            if Maps[x][y] <= 50:
                continue
            ajacent = [0,0,0,0,0,0,0,0]
            try:
                if (Maps[x + 1][y]) >= 200:
                    ajacent[0] = (Maps[x + 1][y])
            except:
                pass
            try:
                if (Maps[x - 1][y]) >= 200:
                    ajacent[0] = (Maps[x - 1][y])
            except:
                pass
            try:
                if (Maps[x][y + 1]) >= 200:
                    ajacent[0] = (Maps[x][y + 1])
            except:
                pass
            try:
                if (Maps[x][y - 1]) >= 200:
                    ajacent[0] = (Maps[x][y - 1])
            except:
                pass
            try:
                if (Maps[x + 1][y + 1]) >= 200:
                    ajacent[0] = (Maps[x + 1][y + 1])
            except:
                pass
            try:
                if (Maps[x - 1][y - 1])>= 200:
                    ajacent[0] = (Maps[x - 1][y - 1])
            except:
                pass
            try:
                if (Maps[x - 1][y + 1])>= 200:
                    ajacent[0] = (Maps[x - 1][y + 1])
            except:
                pass
            try:
                if (Maps[x + 1][y - 1])>= 200:
                    ajacent[0] = (Maps[x + 1][y - 1])
            except:
                pass
            NewMaps[x][y] = (ajacent[0] + ajacent[1] + ajacent[2] + ajacent[3] + ajacent[4] + ajacent[5] + ajacent[6] + ajacent[7] + Maps[x][y]) / 9
    return NewMaps

def gen_map(mapheight, offset, blurs):
    map = numpy.ndarray((mapheight,mapheight))
    for x in range(mapheight):
        for y in range(mapheight):
            map[x][y] = random.random()

    for _ in range(blurs):
        map = blur(map, mapheight)

    for x in range(mapheight):
        for y in range(mapheight):
            #pygame.draw.rect(screen, (round(map[x][y] + offset) * 255,round(map[x][y] + offset) * 255,round(map[x][y] + offset) * 255), ((x * 10, y * 10),(10,10)))
            pygame.draw.rect(screen, (map[x][y] * 255,map[x][y] * 255,map[x][y] * 255), ((x, y),(1,1)))

    return map

new_map = gen_map(800, 0, 100)
print(new_map)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    

    pygame.display.update()
    deltatime = clock.tick(60) / 1000