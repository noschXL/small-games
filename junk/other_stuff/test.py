import pygame
from threading import Thread
from perlin_noise import PerlinNoise
from sys import exit

width = 600
height = 600


pygame.init()
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

noise1 = PerlinNoise(octaves=3)
noise2 = PerlinNoise(octaves=6)
noise3 = PerlinNoise(octaves=12)
noise4 = PerlinNoise(octaves=24)

def gen_row(i, xpix,ypix, offset):
    surf = pygame.Surface((1,1))
    print(offset)
    for j in range(ypix):
        noise_val = noise1([(i - offset)/xpix, j/ypix])
        noise_val += 0.5 * noise2([(i - offset)/xpix, j/ypix])
        noise_val += 0.25 * noise3([(i - offset)/xpix, j/ypix])
        noise_val += 0.125 * noise4([(i - offset)/xpix, j/ypix])
        noise_val = max(noise_val,0)
        noise_val += 0.5
        noise_val *= 255
        surf.fill((255,255,255))
        surf.set_alpha(noise_val)
        screen.blit(surf, ((i+offset,j),(1,1)))

def gen_map(xpix, ypix):
    threads = []
    for i in range(int(xpix / 2)):
        thread = Thread(target=gen_row, args=[i, xpix, ypix])
        threads.append(thread)
        thread.start()

    i = 0
    for thread in threads:
        thread.join()
        print(f"thread {i} is finished")
        i += 1
#curmap = gen_map(600,600)

i = 0
offset = 0
screen.fill((00,255,255))
ipositive = True
moveing = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    gen_row(i,600,600,offset)

    i += 1
    if i >= 600 or moveing:
        moveing = True
        screen.blit(screen,(-1,0))

    pygame.display.flip()
    clock.tick(60)