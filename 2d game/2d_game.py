import pygame,sys,os,numpy

pygame.init()

SIZE = (20,20)

map = numpy.zeros(SIZE)
multiplier = 40

wn = pygame.display.set_mode((SIZE[0]* multiplier, SIZE[0]* multiplier))
clock = pygame.time.Clock()

def load_img(file): 
        img = pygame.image.load(os.path.join(dir, 'img', f'{file}.png'))
        print(f"loaded img: {file}")
        return img

water_img = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        wn.fill(("#000000"))
        for x in range(SIZE[0]):
            for y in range(SIZE[1]):
                pygame.draw.rect(wn, "#B0E0E6", (x * multiplier, y * multiplier, multiplier, multiplier))

        pygame.display.update()
        clock.tick(60)