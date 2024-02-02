import pygame, sys, os, time, random, math

pygame.init()

WIDTH = 600
HEIGHT = 600
SWORD = 1
BOW = 2

wn = pygame.display.set_mode((WIDTH,HEIGHT))
dir = os.path.dirname(os.path.abspath(__file__))
font = pygame.font.Font(os.path.join(dir, 'img', 'font.ttf'))

def load_img(file): 
        img = pygame.image.load(os.path.join(dir, 'img', f'{file}.png'))
        print(f"loaded img: {file}")
        return img

def get_dist(loc1, loc2):
    math.sqrt((abs(loc1[0] - loc2[0]) ** 2 + (loc1[1] - loc2[1])) ** 2)

def draw():
    wn.fill((209, 188, 138)),
    draw_coins(slime_drops, (300,0), coin_imgs[0])
    for mob in slm_drp_lst + mobs + animations:
        if mob is None:
            continue
        mob.draw()

def animate(loc, id, secs):
    anim = Animation(loc, id, secs)
    animations.append(anim)
    return anim

slime_imgs = [load_img("friendly_slime"),
          load_img("raged_slime"),
          load_img("angry_slime"),
          load_img("dead_slime"),
          load_img("flashy_slime")]

coin_imgs = [load_img("slime_drop")]

heart_imgs = [load_img("full_heart"),
              load_img("empty_heart")]

munition_imgs = [load_img("arrow")]

button_imgs = [load_img("old_button")]


def display( text, location, size = 1, color = (0,0,0)):
        text = font.render(str(text), True, color)
        text_rect = text.get_rect(topleft= location)
        text_surface = pygame.Surface((text_rect.width, text_rect.height), pygame.SRCALPHA)
        text_surface.blit(text, (0, 0))
        wn.blit(pygame.transform.scale_by(text_surface, size), text_rect.topleft)

def get_text_width( text, scale = 1):
        text = font.render(str(text), True, (0,0,0))
        text_rect = text.get_rect()
        text_surface = pygame.Surface((text_rect.width, text_rect.height), pygame.SRCALPHA)
        text_surface.blit(text, (0, 0))
        return pygame.transform.scale_by(text_surface, scale).get_width()

def draw_coins(coins, location, sprite: pygame.Surface):
    width = sprite.get_rect().width
    wn.blit(pygame.transform.scale(sprite, (32,32)),location)
    display(coins, (location[0] + width, location[1]), 2)

def draw_hearts(hp,full, location):
    width = pygame.mask.from_surface( pygame.transform.scale(heart_imgs[0], (32,32))).get_size()[0] - 10
    for hrt_cnt in range(hp):
        wn.blit(pygame.transform.scale(heart_imgs[0], (32,32)),(location[0] + width * hrt_cnt, location[1]))
    for hrt_cnt in range(full - hp):
        wn.blit(pygame.transform.scale(heart_imgs[1], (32,32)),(location[0] + width * hrt_cnt + width * hp, location[1]))


#----------------------------------------------
#-------------------CLASSES--------------------
#----------------------------------------------

class SpriteSheet:

    def __init__(self, filename):
        """Load the sheet."""
        self.spritepath = os.path.join(dir,'','img',filename)
        try:
            self.sheet = pygame.image.load(self.spritepath).convert()
            print(f"loaded img: {filename}")
        except pygame.error as err:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(err)

    def image_at(self, rectangle, colorkey = (0,0,0)):
        """Load a specific image from a specific rectangle."""
        # Loads image from x, y, x+offset, y+offset.
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

animation_sheets = [SpriteSheet("slash.png")]

class Animation:
    def __init__(self, loc, id, secs):
        self.loc = loc
        self.ps = len(animations) - 1
        self.id = id
        self.fps = secs
        self.frame = 0
        self.img = pygame.transform.scale(animation_sheets[self.id].image_at((self.frame * 16, 0, 16,16)), (48,48))
        self.time_between_frames = 1 / self.fps #time between frames in secs
        self.timer = Timer(self.new_frame)
        self.timer.start(self.time_between_frames)

    def new_frame(self):
        self.frame += 1
        if self.frame > 5:
            self.timer.stop()
            self.img = pygame.Surface((0,0))
            self.kill()
        else:
            self.img = pygame.transform.scale(animation_sheets[self.id].image_at((self.frame * 16, 0, 16,16)), (48,48))
            self.timer.start(self.time_between_frames)

    def update(self , *args):
        self.timer.update()

    def draw(self):
        wn.blit(self.img, (self.loc))

    def kill(self):
        animations[self.ps] = None


class Shot:
    def __init__ (self, loc, vel, sprite = munition_imgs[0], homing = False, homing_dur = 3,  size = (16,16)):
        self.loc = pygame.Vector2(loc)
        self.vel = vel
        self.homing = homing
        self.homing_dur = homing_dur
        self.timer = Timer(self.homing_off)
        if not self.homing:
            self.timer.start()
        self.sprite = sprite
        self.sprite = pygame.transform.scale(self.sprite, size)
        self.rect = self.sprite.get_rect()
        self.mask = pygame.mask.from_surface(self.sprite)
    
    def update(self, pos):
        if self.homing:
            move_to = [self.loc.x - pos[0], self.loc.y - pos[1]]
            self.loc.x -= move_to[0] / 10
            self.loc.y -= move_to[1] / 10
        else:
            self.loc.x += self.vel[0]
            self.loc.y += self.vel[1]

    def draw(self):
        wn.blit(self.sprite, self.loc.xy)    

    def homing_off(self):
        self.homing = False

class Button:
    def __init__(self,loc, func, img_nmbr = 0, scale = (32, 32)):
        self.sprite = button_imgs[0]
        self.sprite = pygame.transform.scale(self.sprite, scale)
        self.mask = pygame.mask.from_surface(self.sprite)
        self.loc = loc
        self.func = func

    def draw(self):
        wn.blit(self.sprite, self.loc)

    def hit(self, *args):
        self.func()

class Coin:
    def __init__(self, loc , value, type = 0):
        self.loc = loc
        self.value = value
        self.type = type
        self.sprite = coin_imgs[self.type]
        self.sprite = pygame.transform.scale(self.sprite, (25,25))
        self.rect = self.sprite.get_rect()
        self.rect.topleft = loc
        self.mask = pygame.mask.from_surface(self.sprite)
        self.id = len(slm_drp_lst)

    def draw(self):
        wn.blit(self.sprite, self.loc)

    def hit(self, *args):
        global slime_drops
        slm_drp_lst[self.id] = None
        slime_drops += self.value

    def update(self, pos):
        move_to = [self.loc.x - pos [0], self.loc.y - pos[1]]
        self.loc.x -= move_to[0] / 10
        self.loc.y -= move_to[1] / 10

class Mob:
    def __init__(self, loc):
        self.mob_id = len(mobs)
        self.dmg = 0
        self._draw_dmg = False
        self.dmg_loc = (0,0)
        self.dmg_timer = Timer(self.draw_dmg_off)
        self.loc = pygame.Vector2(loc)
        self.vel = pygame.Vector2()
        self.status = random.randint(0,1)
        self.timer = Timer(self.timer_done)
        self.timer.start(3 + random.uniform(-1.0, 1.0)) if self.status == 0 else self.timer.start(1 + random.uniform(-1.0, 1.0))
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

    def update(self, pos):
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
        move_point = (self.loc.x - rect[0], self.loc.y - rect[1])
        move_dist =  0.55 / math.sqrt((self.loc.x - rect[0]) ** 2 + (self.loc.y - rect[1]) ** 2)
        self.vel.move_towards_ip(move_point, move_dist * 1.5)

class Slime(Mob):
    def __init__(self, loc, size = 1):
        super().__init__(loc)
        self.size = size
        self.sprite = self.new_sprite()
        self.rect = self.sprite.get_rect()
        self.rect.topleft = loc
        self.mask = pygame.mask.from_surface(self.sprite)
        self.hp = 20 * self.size

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
                self.animation.kill()
            else:
                self.invulnerable = True
                self.timer.stop()
                self.dmg = damage
                self.dmg_loc = self.rect.topright
                self._draw_dmg = True
                self.dmg_timer.start(1)
                self.animation = animate(self.loc, 0, 45)
                self.flash()
                self.move_in_place(pos)

    def onkill(self):
        if self.size == 1:
            slm_drp_lst.append(Coin(self.loc, random.randint(1,2)))
        elif self.size > 1:
            mobs.append(Slime((self.loc.x + random.uniform(-1.0, 1.0),self.loc.y + random.uniform( a = -1.0,b =  1.0)), self.size - 1))
            mobs.append(Slime((self.loc.x + random.uniform(-1.0, 1.0),self.loc.y + random.uniform(a = -1.0,b = 1.0)), self.size - 1))
            mobs.append(Slime((self.loc.x + random.uniform(-1.0, 1.0),self.loc.y + random.uniform(a = -1.0,b = 1.0)), self.size - 1))
        self.kill()

    def shoot(self):
        move_to = [self.loc.x - pygame.mouse.get_pos()[0], self.loc.y - pygame.mouse.get_pos()[0]]
        self.loc.x -= move_to[0] / 10
        self.loc.y -= move_to[1] / 10

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
            for i in range(10):
                mobs.append(Slime((300 + random.uniform(-1, 1), 300 + random.uniform(-1,1)), 2))
            for i, mob in enumerate(mobs):
                try:
                    if mob is None or mobs[i + 1] is None: 
                        continue
                    mob.move_in_place(mobs[i+1].rect)
                except IndexError as e:
                    pass

    def empty(self):
        gen = (mob for mob in mobs if mob != None)
        if list(gen) == []: return True
        else: return False

class Slime_minigame:

    def __init__(self):
        self.cooldown = Timer(self.mode_switch_allow)
        self.switch = True
        self.rotation = 0
        self.mode = 1
        self.bow_active = False
        self.wave_cnt = 1 # cnt means count
        self.clock = pygame.time.Clock()
        self.wave = Wave(self.wave_cnt)
        self.sword_sprite = pygame.transform.scale(load_img("sword"), (64,64))
        self.bow_sprite = pygame.transform.scale(load_img("bow"), (64,64))
        self.mouse_sprite = self.sword_sprite
        self.mouse_mask = pygame.mask.from_surface(self.mouse_sprite)
        self.mouse_rect = self.mouse_mask.get_rect()
        self.mouse_pos = (0,0)
        self.mouse_status = SWORD
        self.mouse_switch_enabled = True
        self.mouse_switch = Timer(self.enable_switching)
        self.damage = 6
        self.hp = 3
        self.full_hp = 3
        self.fps = 60
        self.restart_button = Button((300 - 32 * 3, 300), self.restart, 0, (64  * 3, 64))
        pygame.mouse.set_visible(False)

    def check_collisions(self, dmg_deal = True):
        for mob in mobs + slm_drp_lst:
            if mob is None:
                continue
            if pygame.Rect.colliderect(mob.sprite.get_rect(), self.mouse_rect):
                offset = [mob.loc[0] - self.mouse_pos[0], mob.loc[1] - self.mouse_pos[1]]
                if self.mouse_mask.overlap(mob.mask, offset):
                    if isinstance(mob, Slime) and mob.status == 2:
                        self.hp -= 1
                    if dmg_deal:
                        mob.hit(self.damage, self.mouse_pos)
                        
    def mode_switch_allow(self):
        self.switch = True
        print("sure")

    def enable_switching(self):
        self.mouse_switch_enabled = True
        self.mouse_switch.stop()

    def check_pressed(self, obj):
        if pygame.mouse.get_pressed(num_buttons= 5)[0]:
            if pygame.Rect.colliderect(obj.sprite.get_rect(), self.mouse_rect):
                offset = [obj.loc[0] - self.mouse_pos[0], obj.loc[1] - self.mouse_pos[1]]
                if self.mouse_mask.overlap(obj.mask, offset):
                    obj.hit(self.damage, self.mouse_pos)

    def update(self, now):
        if now:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
            wn.fill((209,188,138))
            for mob in mobs + slm_drp_lst + animations:
                if mob is None:
                    continue
                mob.update((self.mouse_pos[0] + self.mouse_rect.width / 2, self.mouse_pos[1] + self.mouse_rect.height / 2))
                self.mouse_switch.update()

    def mouse_parsing(self, coll_check = True):
        print(self.switch)
        if self.mode == 0:
            
            self.mouse_pos = pygame.mouse.get_pos()
            wn.blit(self.mouse_sprite,  self.mouse_pos)
            
            if coll_check:
                self.check_collisions()
                
            if pygame.mouse.get_pressed(5)[2] and self.switch:
                self.mode = 1
                self.mouse_sprite = self.bow_sprite
                self.switch = False
                self.cooldown.start(1)
                
        if self.mode == 1:
            
            if self.bow_active:
                pygame.mouse.set_pos(self.mouse_pos)
                if pygame.mouse.get_pressed(5)[0]:
                    heading = [math.cos(self.rotation), math.sin(self.rotation)]
                    shots.append(Shot(self.mouse_pos, heading, munition_imgs[0], size= (32,32)))
                self.bow_active = False
                self.rotation = 0
                
            elif self.bow_active:
                if pygame.mouse.get_pressed(5)[0]:
                    self.bow_active = True
                
                self.mouse_pos = pygame.mouse.get_pos()
                wn.blit(self.mouse_sprite,  self.mouse_pos)
                
            if pygame.mouse.get_pressed(5)[2] and self.switch:
                self.mode = 0
                self.mouse_sprite = self.sword_sprite
                self.switch = False
                self.cooldown.start(1)

    def run(self):
        self.running = True
        while self.running:
            if self.wave.empty():
                self.wave = Wave(self.wave_cnt)
            self.update(True)
            draw()
            draw_hearts(self.hp, self.full_hp, (0,0))
            self.mouse_parsing()
            self.check_kill()
            self.clock.tick(self.fps)
            pygame.display.flip()

        while not self.running:
            wn.fill((0,0,0))
            display("You Died", (300 - get_text_width("You Died",4) / 2, 100), size= 4, color = (255,255,255))
            self.restart_button.draw()
            display("Restart", (300 + 50 - get_text_width("Restart",4) / 2, 300 + 20), size= 2, color = (255,255,255))
            self.check_pressed(self.restart_button)
            self.mouse_parsing(coll_check=False)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.clock.tick(self.fps)


    def check_kill(self):
        if self.hp <= 0:
            self.running = False
            
    def restart(self):
        global slime_drops
        self.__init__()
        mobs.clear()
        shots.clear()
        slm_drp_lst.clear()
        slime_drops = 0
        self.run()

if __name__ == '__main__':
    mobs = []
    shots = []
    animations = []
    slime_drops = 0
    slm_drp_lst = [] # slime_drop_list
    game = Slime_minigame()
    game.run()