import pygame
import os
import sys
import Gui
import grass
import random
from settings import *

pygame.init()

screen = pygame.display.set_mode((width, height))


path = os.path.abspath(os.path.dirname(__file__))

font = pygame.Font(os.path.abspath(os.path.join(path, "..", "data" , "ttf", "prstartk.ttf")))

test_img = pygame.image.load(os.path.abspath(os.path.join(path, "..", "data" , "img", "overlay.png")))
test_img = pygame.transform.scale_by(test_img, 10)

buttons = Gui.RadioButtonGroup()
buttons.add(Gui.ToggleButton(screen, (259, 719 + 20 * 0), "Push", font, False, rounded= 5))
buttons.add(Gui.ToggleButton(screen, (259, 719 + 20 * 1), "Pull", font, False, rounded= 20))
buttons.add(Gui.ToggleButton(screen, (259, 719 + 20 * 2), "Take", font, False, rounded= 20))
buttons.add(Gui.ToggleButton(screen, (259, 719 + 20 * 3), "Use", font, False, rounded= 20))

test = Gui.Dropdown(screen, font=font)

last = 0
while True:
    mousescroll = 0
    mousepress = False
    mousepos = pygame.mouse.get_pos()
    screen.fill("#FFFFFF")

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEWHEEL:
            mousescroll = event.y
            print(mousescroll)

    if pygame.mouse.get_pressed()[0]:
        last = 1
    else:
        if last == 1:
            mousepress = True
        last = 0

    screen.blit(test_img, (0,0))
    buttons.update(mousepos, mousepress)
    buttons.draw()
    if buttons.changed():
        print(buttons.get_active())

    test.update(mousepos, mousepress, mousescroll)
    test.draw()
    pygame.display.flip()