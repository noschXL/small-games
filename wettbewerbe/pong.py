import pygame
from math import sin, cos, radians
from sys import exit

width = 600
height = 600

pygame.init()
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

paddel1_rect = pygame.Rect(70,height / 2 + 5,20, 100)

paddel2_rect = pygame.Rect(530,height / 2 + 5,20, 100)
ball_rect = pygame.Rect(290,290, 10, 10)
ball_velocity = 5
ball_angle = 60

playerpoints = 0
botpoints = 0

while True:
    screen.fill("#000000")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddel1_rect.y -= 5
    if keys[pygame.K_s]:
        paddel1_rect.y += 5

    ball_rect.y += sin(radians(ball_angle)) * ball_velocity
    ball_rect.x += cos(radians(ball_angle)) * ball_velocity

    paddel2_rect.centery -= (paddel2_rect.centery - ball_rect.centery) * 0.1
    if ball_rect.x <= 0:
        botpoints += 1
        ball_rect = pygame.Rect(290,290, 10, 10)
        ball_velocity = 5
        ball_angle = 180
    elif ball_rect.x >= 590:
        botpoints += 1
        ball_rect = pygame.Rect(290,290, 10, 10)
        ball_velocity = 5
        ball_angle = 180
    elif ball_rect.y >= 590:
        ball_rect.y -= sin(radians(ball_angle)) * ball_velocity
        ball_rect.x -= cos(radians(ball_angle)) * ball_velocity
        ball_angle -= 90
    elif ball_rect.y <= 0:
        ball_rect.y -= sin(radians(ball_angle)) * ball_velocity
        ball_rect.x -= cos(radians(ball_angle)) * ball_velocity
        ball_angle += 90
    
    if ball_rect.colliderect(paddel1_rect):
        ball_rect.y -= sin(radians(ball_angle)) * ball_velocity
        ball_rect.x -= cos(radians(ball_angle)) * ball_velocity
        ball_angle += 180
        ball_angle += ball_rect.y - paddel1_rect.y
    if ball_rect.colliderect(paddel2_rect):
        ball_rect.y -= sin(radians(ball_angle)) * ball_velocity
        ball_rect.x -= cos(radians(ball_angle)) * ball_velocity
        ball_angle += 180
        ball_angle += ball_rect.y - paddel2_rect.y

    pygame.draw.rect(screen, "#FFFFFF", paddel1_rect)
    pygame.draw.rect(screen, "#FFFFFF", paddel2_rect)
    pygame.draw.circle(screen, "#FFFFFF", (ball_rect.centerx, ball_rect.centery), 10)

    pygame.display.update()
    clock.tick(60)