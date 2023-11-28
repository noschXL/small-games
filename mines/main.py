import sys, pygame, os
from Spritesheet import *
os.environ['SDL_VIDEO_WINDOW_POS'] = "%i,%i" % (600,300)
os.environ['SDL_VIDEO_CENTERED'] = '0'
pygame.init()
empty = pygame.image.load("img/empty.png")
flag = pygame.image.load("img/flag.png")
mine = pygame.image.load("img/mine.png")
nums = SpriteSheet("numbers.png")
clock = pygame.time.Clock()
colors = [(118, 171, 223),(72, 209, 204),(144, 238, 144),(150, 0, 24)]
move = 0
rows, cols = 8,8

wn = pygame.display.set_mode((cols * 32,rows * 32  + 50))

def changeColor(image, color):
    colouredImage = pygame.Surface(image.get_size())
    colouredImage.fill(color)
    
    finalImage = image.copy()
    finalImage.blit(colouredImage, (0, 0), special_flags = pygame.BLEND_MULT)
    return finalImage

new_pic = changeColor(empty, colors[1])

class field:
    mines = []
    def __init__(self):
        self.show = False
        self.mine = False
        self.flagged = False
        self.near_mines = 0
        self.id = len(field.mines)
        self.x = self.id // rows * 32
        self.y = (self.id % cols * 32) + 50
        self.img = changeColor(empty, colors[0])

    def draw(self):
        if not self.show:
            wn.blit(self.img,(self.x,self.y))
            if self.flagged:
                wn.blit(flag, (self.x,self.y))
        else:
            self.img = changeColor(empty, colors[1])
            wn.blit(empty, (self.x,self.x))
            wn.blit(nums.image_at((12 * (self.mines % 6),12 * (self.mines // 6) , 12,12)), ())
for i in range(rows * cols):
    field.mines.append(field())

def draw_all():
    for square in field.mines:
        square.draw()

def mouse_parse():
    mouse_pos = pygame.mouse.get_pos()
    buttons = pygame.mouse.get_pressed(5)
    square = mouse_pos[0] // 32 + mouse_pos[1] // 32
    if buttons[0]:
        pass
    elif buttons[1]:
        pass

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_parse()
    pygame.key.set_repeat(5,1)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()
    clock.tick(60)
    draw_all()
    pygame.display.flip()