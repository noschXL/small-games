# an attempt to recreate the Pebble app "miner"

import pygame
from sys import exit

width, height = 600,600

gameMap = []
for i in range(width // 10 * height // 10):
    gameMap.append(1)

deltax = 1
deltay = width // 10
pygame.init()
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

current_field = 0
print(len(gameMap))
while True:
    screen.fill("#000000")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    for field, i in enumerate(gameMap):
        if field >= 0:
            pygame.draw.rect(screen, "#FFFFFF", (((field % 60)* 10, (field // 60)* 10),(10,10)))
        

    gameMap[current_field] -= 0.1
    if gameMap[current_field] <= 0:
        current_field += 1
    print(gameMap[current_field])

    pygame.display.update()
    clock.tick(60)