import pygame as pg
import sys,random,math
FPS = 60

RES = (900,900)
AQUA = (0,255,255)
wn = pg.display.set_mode(RES)
GRAVITY = 0
DRAFT = 0.7
COLLISION_DAMPING = 1
SIZE = 10
RADIUS = 100
DOT_SPACE = 50
clock = pg.time.Clock()
DOTS = 50
MASS = 1
MAX_VEL = pg.math.Vector2(50,50)

class fluid:
    dots = []

    def __init__(self,x,y):

        self.position = pg.math.Vector2(x,y)
        self.velocity = pg.math.Vector2()
        self.new_vel = pg.Vector2()
        self.vel_list = []
        self.new_vel_main = pg.Vector2()

    def update(self):
        #self.velocity.y += GRAVITY
        self.evening_out()
        self.velocity * DRAFT
        if self.velocity.x >= MAX_VEL.x:
            self.velocity.x = MAX_VEL.x
        if self.velocity.y >= MAX_VEL.y:
            self.velocity.y = MAX_VEL.y
        self.velocity += self.new_vel_main
        self.position += self.velocity
        fluid.collision(self)
        pg.draw.circle(wn,AQUA,self.position,SIZE)

    def collision(self):
        if self.position.y + self.velocity.y <= 0 + SIZE :
            self.velocity.y -= GRAVITY + 0.1
            self.velocity.y = abs(self.velocity.y)
            self.velocity.y *= COLLISION_DAMPING
        if self.position.y +  self.velocity.y >= 900 - SIZE:
            self.velocity.y -= GRAVITY + 0.1
            self.velocity.y = -abs(self.velocity.y)
            self.velocity.y *= COLLISION_DAMPING
        if self.position.x + self.velocity.x <= 0 + SIZE :
            self.velocity.x = abs(self.velocity.x)
            self.velocity.x *= COLLISION_DAMPING
        if self.position.x + self.velocity.y >= 900 - SIZE:
            self.velocity.x = -abs(self.velocity.x)
            self.velocity.x *= COLLISION_DAMPING

    def evening_out(self):
        self.new_vel = pg.Vector2()
        self.vel_list = []
        self.new_vel_main = pg.Vector2()
        for dot in fluid.dots:
            self.new_vel = pg.Vector2()
            dist = math.sqrt((abs(self.position.x - dot.position.x)) ** 2 + (abs(self.position.y - dot.position.y)) ** 2) #satz des pythagoras
            if dist >= 50 or dist == 0:
                continue
            if -(self.position.x - dot.position.x) != 0:
                self.new_vel.x +=  1 / -(dot.position.x - self.position.x) / 10
            if -(self.position.y - dot.position.y) != 0:
                self.new_vel.y += 1 / -(dot.position.y - self.position.y) / 10
            self.vel_list.append(self.new_vel)
            self.new_vel_main = self.average_vectors(self.vel_list)
            dot.vel_list.append((self.new_vel_main.x / 2, self.new_vel_main.y / 2))

    def average_vectors(self, Vector_list = []):
        x = 0
        y = 0
        if Vector_list == []:
            return (0,0)
        ret_vec = pg.Vector2()
        for vec in Vector_list:
            x += vec.x
            y += vec.y
        ret_vec.x = x / len(Vector_list)
        ret_vec.y = y / len(Vector_list)
        return ret_vec

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
        dot.update()
    pg.display.flip()

while True:
    event_check()

    update()
    clock.tick(FPS)