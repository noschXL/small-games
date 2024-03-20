#inital classes
import pygame
import pytmx
import os
from sys import exit

#class for loading Spritesheets
class SpriteSheet:

    def __init__(self, filename):
        """Load the sheet."""
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)


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

    def images_at(self, rects, colorkey = None):
        """Load a whole bunch of images and return them as a list."""
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey = None):
        """Load a whole strip of images, and return them as a list."""
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)


#Level class
class Level:
    def __init__(self, tilemap, player, visible = True ): 
        #setup
        self.tile_list = []
        self.deco_list = []
        self.interact_list = []
        self.floor2_list = []
        self.visible = visible
        self.tmx_data = pytmx.load_pygame(os.path.join(path, '..', 'img', tilemap))
        self.floor = self.tmx_data.get_layer_by_name("Floor")
        self.floor2 = self.tmx_data.get_layer_by_name("Floor2")
        self.deco = self.tmx_data.get_layer_by_name("Deco")
        self.deco2 = self.tmx_data.get_layer_by_name("Deco2")
        self.interact = self.tmx_data.get_layer_by_name("Interactable")
        self.keys = []

        #defining all tile rects and surfaces(imgs)
        for x,y,surf in self.floor.tiles():
            if surf is None:
                continue
            self.tile_list.append([surf, pygame.Rect(x * 32,y * 32, surf.get_width(), surf.get_height())])

        for x,y,surf in self.deco.tiles():
            self.deco_list.append([surf, pygame.Rect(x * 32,y * 32, surf.get_width(), surf.get_height())])
        for x,y,surf in self.deco2.tiles():
            self.deco_list.append([surf, pygame.Rect(x * 32,y * 32, surf.get_width(), surf.get_height())])

        for x,y,surf in self.interact.tiles():
            self.interact_list.append([surf, pygame.Rect(x * 32,y * 32, surf.get_width(), surf.get_height()), self.tmx_data.get_tile_properties(x,y,2)])
        for x,y,surf in self.floor2.tiles():
            self.floor2_list.append([surf, pygame.Rect(x * 32,y * 32, surf.get_width(), surf.get_height())])

        #reading special values
        for pos in self.interact_list:
            id = pos[2]["id"]
            if id == 1:
                player.spawn(pos[1].topleft)

    def draw(self):
        #draw every tile
        for tile in self.tile_list + self.deco_list + self.interact_list + self.floor2_list:
            screen.blit(tile[0], tile[1])

#player class
class Player:
    def __init__(self, pos):
        self.keys = 0
        self.spawn_pos = pos
        self.walk_frame = 0
        self.idle_frame = 0
        self.spawn()
        self.allow_jump = True
        self.allow_dash = True
        self.direction_x = 1 

    def spawn(self, spawnpos : tuple = None):
        if spawnpos is None:
            self.rect = pygame.Rect((self.spawn_pos), (32,32))
            self.vel = pygame.Vector2(0,0)
            self.frect = pygame.Rect((self.spawn_pos), (32,32))
        else:
            self.spawn_pos = spawnpos
            self.rect = pygame.Rect((self.spawn_pos), (32,32))
            self.vel = pygame.Vector2(0,0)
            self.frect = pygame.Rect((self.spawn_pos), (32,32))


    def draw(self, directions):
        #drawing animation with index
        if directions[0] == 0:
            if self.old_direction == 1:
                self.walk_frame = 0
                self.img = player_idle_img[round(self.idle_frame // 5)]
                self.img.set_colorkey("#FFFFFF")
                screen.blit(self.img, self.rect)
            elif self.old_direction == -1:
                self.walk_frame = 0
                self.img = player_idle_img[round(self.idle_frame // 5) + 6]
                self.img.set_colorkey("#FFFFFF")
                screen.blit(self.img, self.rect)
            else:
                pygame.draw.rect(screen, "#0000FF", self.rect)
        elif directions[0] == 1:
            self.idle_frame = 0
            self.img = player_walk_imgs[round(self.walk_frame // 6)]
            self.img.set_colorkey("#FFFFFF")
            screen.blit(self.img, self.rect)
        elif directions[0] == -1:
            self.idle_frame = 0
            self.img = player_walk_imgs[round(self.walk_frame // 6) + 8]
            self.img.set_colorkey("#FFFFFF")
            screen.blit(self.img, self.rect)
        else:
            pygame.draw.rect(screen, "#00FF00", self.rect)
        

    def update(self, dt, level: Level):
        #animation frames
        self.idle_frame += 1 * dt / 0.0166
        self.idle_frame = self.idle_frame % 30
        self.walk_frame += 1 * dt / 0.0166
        self.walk_frame = self.walk_frame % 24
        new = False

        #movement
        self.old_direction = self.direction_x if self.direction_x != 0 else self.old_direction
        self.direction_x = 0
        self.direction_y = 0
        self.entering = False
        self.using = False
        self.jumping = 0
        self.dashing = False
        self.vel.x *= 0.8

        # input
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction_x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction_x += 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.direction_y += 1
        if keys[pygame.K_SPACE]  or keys[pygame.K_UP]:
            self.direction_y -= 1
            if self.allow_jump and self.vel.y == 0:
                self.jumping = 1
                self.allow_jump = False
        if (keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]) and self.allow_dash and abs(self.vel.x) <= 6:
            self.dashing = True
            self.allow_dash = False
        if keys[pygame.K_e] or keys[pygame.K_w]:
            self.using = True

        #velocity + input
        self.vel.x += (1 * dt / 0.0166) * self.direction_x
        self.vel.y -= (12.5 * dt / 0.0166) * self.jumping
        if self.dashing:
            if self.direction_x != 0:
                self.vel.x = 100 * self.direction_x * dt /0.0166
                self.vel.y = 0
            if self.direction_y != 0:
                self.vel.y = 100 * self.direction_y * dt /0.0166

        # clamping to min and max
        self.vel.x = pygame.math.clamp(self.vel.x, -15, 20)
        self.vel.y = pygame.math.clamp(self.vel.y, -15, 20)

        #gravity
        self.vel.y += 1 * dt / 0.0166

        if abs(self.vel.x) <= 0.1:
            self.vel.x = 0 

        dx = round(self.vel.x)
        dy = round(self.vel.y)


        for tile in level.tile_list + level.floor2_list:

            #y collision
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                #below ground
                if self.vel.y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel.y = 0
                #above ground
                elif self.vel.y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel.y = 0
                    self.allow_jump = True
                    self.allow_dash = True
                
            #x collision
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                dx = 0
                self.vel.x = 0

    
        for tile in level.interact_list:
            if tile[1].colliderect(self.rect):
                id = tile[2]["id"]
                if id == 0 and self.using:
                    new = 1
                elif id ==5 and self.using:
                    new = 1
                elif id ==8:
                    self.spawn()
                else:
                    pass

        # update position
        self.rect.x += dx
        self.rect.y += dy
        if self.rect.y >= height:
            self.spawn()

        self.draw((self.direction_x, self.direction_y))
        return new

def main():
    current_level = 0
    player = Player((width / 2, height / 2))
    level = Level(level_file_dict[levellist[current_level]], player)

    #Game loop
    while True:
        #deltatime and stable Fps
        dt = clock.tick(60) / 1000
        #event_check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        #blank screen
        screen.fill("#00FFFF")

        #drawing and updateing
        level.draw()
        adding = player.update(dt, level)
        if adding:
            if current_level + adding >= 5:
                current_level = 3
            else:
                current_level += adding
            level = Level(level_file_dict[levellist[current_level]], player)

        
        #screen refresh
        pygame.display.flip()

#initial setup
width, height = 1280, 800
path = os.path.abspath(__file__)
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# defining spritesheets and imgs
player_walk = SpriteSheet(os.path.join(path, '..', 'img', 'character_walk.png'))
player_idle = SpriteSheet(os.path.join(path, '..', 'img', 'character_idle.png'))
player_walk_imgs = []
level_file_dict = {
    "tutorial": "lvl_1.tmx",
    "level_2": "lvl_2.tmx",
    "level_3": "lvl_3.tmx",
    "level_4": "school_floor.tmx",
    "level_5": "classroom_1.tmx"
}

levellist = ["tutorial", "level_2", "level_3", "level_4", "level_5"]

for y in range(4):
    player_walk_imgs += player_walk.load_strip((0,32 * y, 32, 32), 4)

player_idle_img = []
for y in range(2):
    player_idle_img += player_idle.load_strip((0,32 * y, 32, 32), 6)

#player- and levelloading

#running the game
if __name__ == "__main__":
    main()