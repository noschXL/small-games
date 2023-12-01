import pygame, sys, os, time, random, math

pygame.init()

WIDTH = 600
HEIGHT = 600


wn = pygame.display.set_mode((WIDTH,HEIGHT))
dir = os.path.dirname(os.path.abspath(__file__))
font = pygame.font.Font(os.path.join(dir, 'img', 'font.ttf'))

def changeColor(image, color):
    colouredImage = pygame.Surface(image.get_size())
    colouredImage.fill(color)
    
    finalImage = image.copy()
    finalImage.blit(colouredImage, (0, 0), special_flags = pygame.BLEND_MULT)
    return finalImage

def load_img(file):
        img = pygame.image.load(os.path.join(dir, 'img', f'{file}.png'))
        print(f"loaded img: {file}")
        return img

def get_dist(loc1, loc2):
    math.sqrt((abs(loc1[0] - loc2[0]) ** 2 + (loc1[1] - loc2[1])) ** 2)

def draw():
    wn.fill((209, 188, 138))
    for mob in mobs:
        if mob is None:
            continue
        mob.draw()

slime_imgs = [load_img("friendly_slime"),
          load_img("raged_slime"),
          load_img("angry_slime"),
          load_img("dead_slime"),
          load_img("flashy_slime")]

heart_imgs = [load_img("full_heart"),
              load_img("empty_heart")]


def display( number, location):
        text = font.render(str(number), True, (255, 255, 255))
        text_rect = text.get_rect(center=location)
        text_surface = pygame.Surface((text_rect.width, text_rect.height), pygame.SRCALPHA)
        text_surface.blit(text, (0, 0))
        wn.blit(text_surface, text_rect.topleft)

#----------------------------------------------
#-------------------CLASSES--------------------
#----------------------------------------------

class Coin:
    def __init__(self, loc , value):
        self.loc = loc

class Mob:
    def __init__(self, loc):
        self.mob_id = len(mobs)
        self.dmg = 0
        self._draw_dmg = False
        self.dmg_loc = (0,0)
        self.dmg_timer = Timer(self.draw_dmg_off)
        self.loc = pygame.Vector2(loc)
        self.vel = pygame.Vector2()
        self.status = 0
        self.timer = Timer(self.timer_done)
        self.timer.start(3)
        self.inv_timer = Timer(self.flash)
        self.invulnerable = False
        self.got_flashed = 0
    
    def timer_done(self):
        self.status = (self.status + 1) % 3
        if self.status == 0:
            self.timer.start(3 + random.uniform(-1.0, 1.0))
        elif self.status == 1:
            self.timer.start(1 + random.uniform(-1.0, 1.0))
        elif self.status == 2:
            self.timer.start(1 + random.uniform(-1.0, 1.0))
        self.after_timer()

    def draw(self):
        wn.blit(self.sprite, self.loc)
        self.draw_dmg()

    def kill(self):
        mobs[self.mob_id] = None

    def draw_dmg(self):
        if self._draw_dmg:
            display(self.dmg, self.dmg_loc)

    def draw_dmg_off(self):
        self._draw_dmg = False
        self.dmg_timer.stop()

    def after_timer(self):
        pass

    def flash(self):
        pass

    def update(self):
        self.timer.update()
        self.inv_timer.update()
        self.dmg_timer.update()
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y
        for mob in mobs:
            if mob is not None and mob.mob_id != self.mob_id:
                offset = [mob.loc[0] - self.loc[0], mob.loc[1] - self.loc[1]]
                if self.mask.overlap(mob.mask, offset):
                    self.move_in_place(mob.rect)
        self.loc.x += self.vel.x
        self.loc.y += self.vel.y
        if self.loc.x <= 0 +  self.rect.width:
            self.vel.x = -self.vel.x
            self.loc.x += self.vel.x + 1
        if self.loc.x >= WIDTH -  self.rect.width:
            self.vel.x = -self.vel.x
            self.loc.x += self.vel.x + 1
        if self.loc.y <= 0 +  self.rect.height:
            self.vel.y = -self.vel.y
            self.loc.x += self.vel.y + 1
        if self.loc.y >= HEIGHT -  self.rect.height:
            self.vel.y = -self.vel.y
            self.loc.x += self.vel.y + 1
        self.vel.x *= 0.85
        self.vel.y *= 0.85


    def move_in_place(self, rect: pygame.Rect):
        #x_mov = (self.rect.x + self.rect.width) if self.loc.x < rect.x else self
        move_point = (self.loc.x - rect[0], self.loc.y - rect[1])
        move_dist =  0.55 / math.sqrt((self.loc.x - rect[0]) ** 2 + (self.loc.y - rect[1]) ** 2)
        self.vel.move_towards_ip(move_point, move_dist)

class Slime(Mob):
    def __init__(self, loc, size = 1):
        super().__init__(loc)
        self.size = size
        self.sprite = self.new_sprite()
        self.rect = self.sprite.get_rect()
        self.rect.topleft = loc
        self.mask = pygame.mask.from_surface(self.sprite)
        self.hp = 10 * self.size

    def after_timer(self):
        self.sprite = self.new_sprite()

    def new_sprite(self):
        sprite = pygame.transform.scale(slime_imgs[self.status],( (2**5) + self.size * 5,  (2**5) + self.size * 5))
        return sprite

    def flash(self):
        if self.got_flashed == 0 or self.got_flashed == 2:
            self.status = 4
            self.sprite = self.new_sprite()
            self.inv_timer.start(0.15)
            self.got_flashed += 1
        elif self.got_flashed == 1:
            self.status = 0
            self.sprite = self.new_sprite()
            self.got_flashed += 1
            self.inv_timer.start(0.2)
        elif self.got_flashed == 3:
            self.inv_timer.stop()
            self.status = 0
            self.sprite = self.new_sprite()
            self.invulnerable = False
            self.timer.start(3)

    def hit(self, damage, pos):
        if self.invulnerable:
            pass
        else:
            self.hp -= damage
            if self.hp <= 0:
                self.status = 3
                self.sprite = self.new_sprite()
                self.timer = Timer(self.onkill)
                self.timer.start(0.5)
            else:
                self.invulnerable = True
                self.timer.stop()
                self.dmg = damage
                self.dmg_loc = self.rect.topright
                self._draw_dmg = True
                self.dmg_timer.start(1)
                self.flash()
                self.move_in_place(pos)

    def onkill(self):
        if self.size > 1:
            mobs.append(Slime((self.loc.x + random.uniform(-1.0, 1.0),self.loc.y + random.uniform( a = -1.0,b =  1.0)), self.size - 1))
            mobs.append(Slime((self.loc.x + random.uniform(-1.0, 1.0),self.loc.y + random.uniform(a = -1.0,b = 1.0)), self.size - 1))
            mobs.append(Slime((self.loc.x + random.uniform(-1.0, 1.0),self.loc.y + random.uniform(a = -1.0,b = 1.0)), self.size - 1))
        self.kill()

class Timer:
    def __init__(self, func):
        self.func = func
        self.running = False

    def start(self, seconds):
        """Start a new timer"""
        self.running = True
        self.secs = seconds
        self._start_time = time.perf_counter()

    def update(self):
        if self.running:
            if time.perf_counter() - self._start_time >= self.secs:
                self.func()

    def stop(self):
        self.running = False

class Wave:
    def __init__(self, wave):
        if wave == 1:
            mobs.append(Slime((300 + random.uniform(-1, 1), 300 + random.uniform(-1,1)), 2))
            mobs.append(Slime((300 + random.uniform(-1, 1), 300 + random.uniform(-1,1)), 2))
            mobs.append(Slime((300 + random.uniform(-1, 1), 300 + random.uniform(-1,1)), 2))
            mobs.append(Slime((300 + random.uniform(-1, 1), 300 + random.uniform(-1,1)), 2))
            mobs.append(Slime((300 + random.uniform(-1, 1), 300 + random.uniform(-1,1)), 2))
            mobs.append(Slime((300 + random.uniform(-1, 1), 300 + random.uniform(-1,1)), 2))
            mobs.append(Slime((300 + random.uniform(-1, 1), 300 + random.uniform(-1,1)), 2))
            mobs.append(Slime((300 + random.uniform(-1, 1), 300 + random.uniform(-1,1)), 2))
            mobs.append(Slime((300 + random.uniform(-1, 1), 300 + random.uniform(-1,1)), 2))
            mobs.append(Slime((300 + random.uniform(-1, 1), 300 + random.uniform(-1,1)), 2))
            for i, mob in enumerate(mobs):
                try:
                    print("tried")
                    if mob is None: continue
                    mob.move_in_place(mobs[i+1].rect)
                except IndexError as e:
                    print(f"didnt_work :( because of {e}")

    def empty(self):
        gen = (mob for mob in mobs if mob != None)
        if list(gen) == []: return True
        else: return False

class Game:

    def __init__(self):
        self.wave_cnt = 1 # cnt means count
        self.clock = pygame.time.Clock()
        self.wave = Wave(self.wave_cnt)
        self.mouse_sprite = pygame.transform.scale(load_img("sword"), (64,64))
        self.mouse_mask = pygame.mask.from_surface(self.mouse_sprite)
        self.mouse_rect = self.mouse_mask.get_rect()
        self.damage = 6
        self.hp = 3
        self.fps = 60
        pygame.mouse.set_visible(False)

    def check_collisions(self):
        for mob in mobs:
            if mob is None:
                continue
            if pygame.Rect.colliderect(mob.sprite.get_rect(), self.mouse_rect):
                offset = [mob.loc[0] - self.mouse_pos[0], mob.loc[1] - self.mouse_pos[1]]
                if self.mouse_mask.overlap(mob.mask, offset):
                    mob.hit(self.damage, self.mouse_pos)

    def update(self, now):
        if now:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            wn.fill((209,188,138))

            for mob in mobs:
                if mob is None:
                    continue
                mob.update()

    def mouse_parsing(self):
        self.mouse_pos = pygame.mouse.get_pos()
        wn.blit(self.mouse_sprite,  self.mouse_pos)
        self.check_collisions()

    def run(self):
        while True:
            now = True
            if self.wave.empty():
                self.wave = Wave(self.wave_cnt)

            self.update(now)
            draw()
            self.mouse_parsing()
            self.clock.tick(self.fps)
            pygame.display.flip()


if __name__ == '__main__':
    mobs = []
    money = 0
    game = Game()
    game.run()