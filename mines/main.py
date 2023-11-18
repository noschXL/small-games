import sys, pygame, os
from Spritesheet import *
os.environ['SDL_VIDEO_WINDOW_POS'] = "%i,%i" % (600,300)
os.environ['SDL_VIDEO_CENTERED'] = '0'
pygame.init()
empty = pygame.image.load("img/empty.png")
clock = pygame.time.Clock()
colors = [(144, 238, 144),(255,0,0)]

wn = pygame.display.set_mode((512,512))

def changColor(image, color):
    colouredImage = pygame.Surface(image.get_size())
    colouredImage.fill(color)
    
    finalImage = image.copy()
    finalImage.blit(colouredImage, (0, 0), special_flags = pygame.BLEND_MULT)
    return finalImage

new_pic = changColor(empty, colors[1])

class field:
    def __init__(self):
        self.mine = False
        self.near_mines = 0


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.key.set_repeat(5,1)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()
    clock.tick(60)
    wn.blit(new_pic, (0,0))
    pygame.display.flip()