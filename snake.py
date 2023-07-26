import pygame,sys

wn = pygame.display.set_mode((600, 600))
pygame.display.set_caption("snake")

_GREEN =

class snake:
    snaketails = []
    def __init__(self):
        self.posX = 300
        self.posY = 300
        self.direction = 2
        self.rect = pygame.rect.Rect(300,300,30,30)
        self.img = pygame.draw.rect(wn,"lime",self.rect)


while True:

        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                  pygame.quit()
                  sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.direction = 1