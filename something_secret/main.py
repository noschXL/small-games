import pygame, sys, os, time, random

pygame.init()

wn = pygame.display.set_mode((600,600))

def load_img(file):
        img = pygame.image.load(os.path.abspath(__file__)+ "\..\img\\"+ file + ".png")
        print(f"loaded img: {file}")
        return img

def draw():
    for mob in mobs:
        if mob is None:
            continue
        mob.draw()

slime_imgs = [load_img("friendly_slime"),
          load_img("raged_slime"),
          load_img("angry_slime")]

heart_imgs = [load_img("full_heart"),
              load_img("empty_heart")]

class Mob:
    def __init__(self, loc):
        self.mob_id = len(mobs)
        self.loc = loc
        self.status = 0
        self.timer = Timer(self.timer_done)
        self.timer.start(3)
    
    def timer_done(self):
        self.status = (self.status + 1) % 3
        if self.status == 0:
            self.timer.start(4 + random.uniform(-1.0, 1.0))
        elif self.status == 1:
            self.timer.start(2 + random.uniform(-1.0, 1.0))
        elif self.status == 2:
            self.timer.start(2 + random.uniform(-1.0, 1.0))
        self.after_timer()

    def draw(self):
        wn.blit(self.sprite, self.loc)

    def kill(self):
        mobs[self.mob_id] = None

class Wave:
    def __init__(self, wave):
        if wave == 1:
            self.enemys = 1
            mobs.append(Slime((300, 300)))


class Game:

    def __init__(self):
        self.wave = 1
        self.clock = pygame.time.Clock()
        Wave(self.wave)
        self.mouse_sprite = pygame.transform.scale(load_img("sword"), (64,64))
        self.mouse_mask = pygame.mask.from_surface(self.mouse_sprite)
        self.mouse_rect = self.mouse_mask.get_rect()
        self.hp = 3
        pygame.mouse.set_visible(False)

    def check_collisions(self, mouse_pos):
        for mob in mobs:
            if mob is None:
                continue
            offset = [mob.loc[0] - self.mouse_pos[0], mob.loc[1] - self.mouse_pos[1]]
            if self.mouse_mask.overlap(mob.mask, offset):
                print("hit")
                mob.kill()

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
                mob.timer.update()

    def mouse_parsing(self):
        self.mouse_pos = pygame.mouse.get_pos()
        wn.blit(self.mouse_sprite,  self.mouse_pos)
        self.check_collisions(self.mouse_pos)
        pygame.display.flip()


    def run(self):
        while True:
            now = True
            self.update(now)
            draw()
            self.mouse_parsing()
            pygame.display.flip()
            

class Slime(Mob):
    def __init__(self, loc, size = 1):
        super().__init__(loc)
        self.size = size
        self.new_sprite()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.sprite)


    def after_timer(self):
        self.new_sprite()

    def new_sprite(self):
        self.image = pygame.transform.scale(slime_imgs[self.status],( (2**6) + self.size * 5,  (2**6) + self.size * 5))
        self.sprite = pygame.transform.scale(slime_imgs[self.status],( (2**6) + self.size * 5,  (2**6) + self.size * 5))
        
class Timer:
    def __init__(self, func):
        self.func = func

    def start(self, seconds):
        """Start a new timer"""
        self.secs = seconds
        self._start_time = time.perf_counter()

    def update(self):
        if time.perf_counter() - self._start_time >= self.secs:
            self.func()

mobs = []

if __name__ == '__main__':
     game = Game()
     game.run()