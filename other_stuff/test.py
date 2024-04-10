import sys
import pygame

pygame.init()

screen = pygame.display.set_mode((600,600))

x = 300
y = 300
speed = 3
rect = pygame.Rect(x,y,40,80)
clock = pygame.Clock()

while True:
    screen.fill("#000000")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_w]:
        rect.y -= speed
    if keys[pygame.K_a]:
        rect.x -= speed
    if keys[pygame.K_s]:
        rect.y += speed
    if keys[pygame.K_d]:
        rect.x += speed
        
    pygame.draw.rect(screen, "#FF0000", rect)
    pygame.display.flip()
    
    clock.tick(60)