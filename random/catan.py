import pygame
import math
from sys import exit


pygame.init()

width, height = 600,600

screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

pointa = (width / 2, height / 2)
angles = [0,60,120,180,240,300, 360]

points = []
for angle in angles:
    points.append((math.cos(math.radians(angle)) * 100 + pointa[0], math.sin(math.radians(angle)) * 100 + pointa[1]))

points.append(points[-1])
hexrect = pygame.Rect(200, 213, 201, 174)
pygame.draw.polygon(screen, "#FFFFFF", points)

class Hexagon:
    def __init__(self, color, middle):
        self.color = color
        self.surface = pygame.Surface(201, 174)
        points = []
        angles = [0,60,120,180,240,300, 360]
        for angle in angles:
            points.append((math.cos(math.radians(angle)) * 100 + pointa[0], math.sin(math.radians(angle)) * 100 + pointa[1]))
        self.rect = pygame.draw.polygon(self.surface, "#FFFFFF", points)
        self.rect.center = middle

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


    pygame.display.update()
    clock.tick(60)