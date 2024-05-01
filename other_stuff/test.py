import pygame
from threading import Thread
import queue
from perlin_noise import PerlinNoise
from sys import exit

width = 600
height = 600

class ReturnableThread(Thread):
    # This class is a subclass of Thread that allows the thread to return a value.
    def __init__(self,group = None, target = None, name = None, daemon = None,*args, **kwargs):
        Thread.__init__(self, group, target, name, args, kwargs, deamon) # type: ignore
        self.target = target
        self.result = None
    
    def run(self) -> None:
        self.result = self.target()

pygame.init()
screen = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

noise1 = PerlinNoise(octaves=3)
noise2 = PerlinNoise(octaves=6)
noise3 = PerlinNoise(octaves=12)
noise4 = PerlinNoise(octaves=24)

def gen_row(i, xpix,ypix):
    for j in range(ypix):
        noise_val = noise1([i/xpix, j/ypix])
        noise_val += 0.5 * noise2([i/xpix, j/ypix])
        noise_val += 0.25 * noise3([i/xpix, j/ypix])
        noise_val += 0.125 * noise4([i/xpix, j/ypix])
        noise_val = abs(noise_val)
        noise_val += 0.35

    return [(round(noise_val) * 255,round(noise_val) * 255,round(noise_val) * 255), ((i * 1,j * 1),(1,1))]

def gen_map(xpix, ypix):
    threads = []
    retmap = []
    for i in range(xpix):
        thread = ReturnableThread(target=gen_row, args=[i, xpix, ypix])
        threads.append(thread)
        thread.start()

    i = 0
    for thread in threads:
        thread.join()
        retmap.append(thread.result)
        print(f"thread {i} is finished")
        i += 1
    return retmap

curmap = gen_map(600,600)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


    for colum, row in enumerate(curmap):
        pygame.draw.rect(screen, colum[0], colum[1])


    pygame.display.flip()
    clock.tick(60)