import pygame
from sys import exit


pygame.init()
wn = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 16)



def display(number, location):
    text = font.render(str(number), True, (255, 255, 255))
    text_rect = text.get_rect(center=location)
    pygame.draw.rect(wn, (209, 188, 138), text_rect)  # Fill background rectangle
    wn.blit(text, text_rect.topleft)
    pygame.display.update(text_rect)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        wn.fill((209, 188, 138)) 
        display(6, (300,300))


        pygame.display.update()
        clock.tick(60)