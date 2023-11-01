import pygame as pg
import sys,random,math
FPS = 60

RES = (900,900)
AQUA = (0,255,255)
wn = pg.display.set_mode(RES)
GRAVITY = 0.45
DRAFT = 50000
COLLISION_DAMPING = 0.9
SIZE = 10
RADIUS = 100
DOT_SPACE = 50
clock = pg.time.Clock()
DOTS = 10
MASS = 1
MAX_VEL = pg.math.Vector2(50,50)


class fluid:
    dots = []

    def __init__(self,x,y):

        self.position = pg.math.Vector2(x,y)
        self.velocity = pg.math.Vector2()

    def update(self):
        self.velocity.y += GRAVITY
        self.velocity / DRAFT
        if self.velocity.x >= MAX_VEL.x:
            self.velocity.x = MAX_VEL.x
        if self.velocity.y >= MAX_VEL.y:
            self.velocity.y = MAX_VEL.y
        self.position += self.velocity
        fluid.collision(self)
        pg.draw.circle(wn,AQUA,self.position,SIZE)

    def collision(self):
        if self.position.y <= 0 + SIZE :
            self.velocity.y -= GRAVITY + 0.1
            self.velocity.y = abs(self.velocity.y)
            self.velocity.y *= COLLISION_DAMPING
        if self.position.y >= 900 - SIZE:
            self.velocity.y -= GRAVITY + 0.1
            self.velocity.y = -abs(self.velocity.y)
            self.velocity.y *= COLLISION_DAMPING
        if self.position.x <= 0 + SIZE :
            self.velocity.x = abs(self.velocity.x)
            self.velocity.x *= COLLISION_DAMPING
        if self.position.x >= 900 - SIZE:
            self.velocity.x = -abs(self.velocity.x)
            self.velocity.x *= COLLISION_DAMPING

    def evening_out(self):
        new_vel = pg.Vector2()
        new_vel_main = pg.Vector2()
        for dot in fluid.dots:
            if abs(self.position - dot.position)

    def average_vectors(self, Vector1,Vector2):
        return (Vector1 + Vector2) / 2

    def smoothing_kernel(self,dst):
        volume = math.pi * pow(RADIUS, 8) / 4
        value = max(0, RADIUS * RADIUS - dst * dst)
        return value * value / volume

    def calc_density(self):
        density = 0
        for dot in fluid.dots:
            position = dot.position
            dst = pg.math.Vector2.magnitude(position - self.position)
            influence = self.smoothing_kernel(dst)
            density += MASS + influence
        return density
    def calc_property(self):
        prop = 0
        for dot in fluid.dots:
            position = dot.position
            dst = pg.math.Vector2.magnitude(position - self.position)
            influence = self.smoothing_kernel(dst)
            prop += 1

dots_per_row = math.sqrt(DOTS)
dots_per_col = (DOTS - 1) / dots_per_row + 1
spacing = SIZE * 2 + DOT_SPACE

for i in range(DOTS):
    x = 450 + ((i % dots_per_row - dots_per_row / 2 + 0.5) * DOT_SPACE)
    y = 450 + ((i / dots_per_row - dots_per_col / 2 + 0.5) * DOT_SPACE)
    fluid.dots.append(fluid(x,y))

def event_check():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

def update():
    wn.fill((0,0,0))
    for dot in fluid.dots:
        dot.evening_out()
        dot.update()
    pg.display.flip()

while True:
    event_check()

    update()
    clock.tick(FPS)