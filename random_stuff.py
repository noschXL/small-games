import pygame
import numpy
import random
import time
from sys import exit


width = 800
height = 800
pygame.init()
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

MAP_HEIGHT = 80

Maps = numpy.ndarray((MAP_HEIGHT,MAP_HEIGHT))
NewMaps = numpy.ndarray((MAP_HEIGHT,MAP_HEIGHT))
for x in range(MAP_HEIGHT):
    for y in range(MAP_HEIGHT):
        Maps[x][y] = random.uniform(0.0,255.0)

NewMaps = Maps

def blur():
    for x in range(MAP_HEIGHT):
        for y in range(MAP_HEIGHT):
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

blur()
blur()
blur()
blur()
blur()
blur()
blur()
blur()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    for x in range(MAP_HEIGHT):
        for y in range(MAP_HEIGHT):
            pygame.draw.rect(screen, (NewMaps[x][y],NewMaps[x][y],NewMaps[x][y]), ((x * 10, y * 10),(10,10)))

    pygame.display.update()
    deltatime = clock.tick(60) / 1000