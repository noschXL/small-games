import pygame
import os
import sys
import Gui
from settings import *

pygame.init()

screen = pygame.display.set_mode((width, height))


path = os.path.abspath(os.path.dirname(__file__))

font = pygame.Font(os.path.abspath(os.path.join(path, "..", "data" , "ttf", "prstartk.ttf")))

test_img = pygame.image.load(os.path.abspath(os.path.join(path, "..", "data" , "img", "overlay.png")))
test_img = pygame.transform.scale_by(test_img, 10)

buttons = [Gui.Button(screen, (259, 719 + 20 * 0), "Push", font, False, rounded= 5),
           Gui.Button(screen, (259, 719 + 20 * 1), "Pull", font, False, rounded= 20),
           Gui.Button(screen, (259, 719 + 20 * 2), "Take", font, False, rounded= 5),
           Gui.Button(screen, (259, 719 + 20 * 3), "Use", font, False, rounded= 20)]
while True:
    screen.fill("#FFFFFF")
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(test_img, (0,0))
    mousepos = pygame.mouse.get_pos()
    for button in buttons:
        button.update(mousepos)
        button.draw()
    pygame.display.flip()