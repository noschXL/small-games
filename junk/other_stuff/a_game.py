import pygame, sys

pygame.init()

width, height = 1280, 800
screen = pygame.display.set_mode((width, height))

print(screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT():
            pygame.quit()
            sys.exit()