#inital classes
import pygame
import pytmx
import math
import os
import sys
import random
#set to True when compiling using pyinstaller --noconsole --onefile 'main.py' else set it to False to run the programm 
COMPILING = False

def resource_path(relative_path):
    try:
        latestbs = None
        for char, i in enumerate(sys.executable):
            if char == "\\":
                latestbs = i
        base_path = sys.executable[latestbs]
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#function for separating text
def sep_text(text: str, breakpoint = 10):
    spaces = []
    texts = []
    posi = 1
    old_space = 0
    for i,char in enumerate(text):
        if char.isspace():
            spaces.append(i)
    
    for space in spaces:
        if space // breakpoint >= posi:
            posi += 1
            texts.append(text[old_space:space])
            old_space = space
            
    texts.append(text[old_space:])
    return texts

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
        self.enemy_list = []
        self.enemys = []
        self.texts = []
        self.visible = visible
        if COMPILING:
            self.tmx_data = pytmx.load_pygame(tilemap)
        else:
            self.tmx_data = pytmx.load_pygame(os.path.join(path, "img", tilemap))
        self.floor = self.tmx_data.get_layer_by_name("Floor")
        self.floor2 = self.tmx_data.get_layer_by_name("Floor2")
        self.deco = self.tmx_data.get_layer_by_name("Deco")
        self.deco2 = self.tmx_data.get_layer_by_name("Deco2")
        self.interact = self.tmx_data.get_layer_by_name("Interactable")
        self.enemy = self.tmx_data.get_layer_by_name("Enemy")
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
            self.interact_list.append([surf, pygame.Rect(x * 32,y * 32, surf.get_width(), surf.get_height()), self.tmx_data.get_tile_properties(x,y,3)])
        for x,y,surf in self.floor2.tiles():
            self.floor2_list.append([surf, pygame.Rect(x * 32,y * 32, surf.get_width(), surf.get_height())])
        for x,y,surf in self.enemy.tiles():
            self.enemy_list.append([surf, pygame.Rect(x * 32,y * 32, surf.get_width(), surf.get_height()), self.tmx_data.get_tile_properties(x,y,0)])

        #reading special values
        for pos in self.interact_list:
            id = pos[2]["id"]
            if id == 1:
                player.spawn(pos[1].topleft)

        for enemy in self.enemy_list:
            if enemy[2]["id"] == 2:
                self.texts.append(Text(enemy[2]["text"], enemy[1].topleft, 0.5))
            else:
                self.enemys.append(Enemy(enemy[1].topleft))
        
    def draw(self, dt):
        #draw every tile
        for tile in self.tile_list + self.deco_list + self.interact_list + self.floor2_list:
            screen.blit(tile[0], tile[1])
        #draw enemys
        for enemy in self.enemys:
            enemy.draw(dt)
        #draw text
        for text in self.texts:
            text.draw()

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
        self.beaten = 0
        self.not_beaten = 0

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


    def draw(self, directions, dt):
        #animation frames
        self.idle_frame += 1 * dt / 0.0166
        self.idle_frame = self.idle_frame % 30
        self.walk_frame += 1 * dt / 0.0166
        self.walk_frame = self.walk_frame % 24
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
                elif id == 4 and self.using:
                    new = 2
                elif id ==8:
                    self.spawn()
                else:
                    pass
                
        for enemy in level.enemys:
            if enemy.rect.colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height) and not enemy.defeated:
                dx = 0
                self.vel.x = 0
                if self.using:
                    beaten = enemy.interact(self, level)
                    if beaten is None:
                        pass
                    elif beaten:
                        self.beaten += 1
                    else:
                        self.not_beaten += 1
                        
            if enemy.rect.colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height) and not enemy.defeated:
                dy = 0
                self.vel.y = 0
                self.allow_jump = True
                self.allow_dash = True

        # update position
        self.rect.x += dx
        self.rect.y += dy
        if self.rect.y >= height:
            self.spawn()

        self.draw((self.direction_x, self.direction_y), dt)
        return new
    
    def the_end(self):
        Endscreen(self.beaten, self.not_beaten)

#enemy class
class Enemy:
    def __init__(self, pos: tuple):
        self.defeated = False
        self.rect = pygame.rect.Rect(pos,(32,32))
        self.frame = 0
        self.likeing = 0
        self.idle_frame = 0
        if random.random:
            self.old_direction = 1
        else:
            self.old_direction = -1
        
    def draw(self, dt):
        self.idle_frame += 1 * dt / 0.0166
        self.idle_frame = self.idle_frame % 30
        if self.old_direction == 1:
            self.walk_frame = 0
            self.img = npc_idle_img[round(self.idle_frame // 5)]
            self.img.set_colorkey("#FFFFFF")
            screen.blit(self.img, self.rect)
        elif self.old_direction == -1:
            self.walk_frame = 0
            self.img = npc_idle_img[round(self.idle_frame // 5) + 6]
            self.img.set_colorkey("#FFFFFF")
            screen.blit(self.img, self.rect)
    
    def interact(self, player: Player, level: Level):
        return interact_entity(self, player, level)
        
#text class
class Text:
    
    def __init__(self, text: str, pos: tuple, scale, color = "#000000", breakpoint = 10):
        
        last_height = 0
        self.rects = []
        self.surfaces = []
        texts = sep_text(text, breakpoint)
        
        for string in texts:
            surface = font.render(string, False, color)
            surface = pygame.transform.scale_by(surface, scale)
            rect = surface.get_rect()
            rect.centerx = pos[0]
            rect.top = pos[1] + last_height + 5
            last_height = rect.bottom - pos[1]
            self.surfaces.append(surface)
            self.rects.append(rect)
        
    def draw(self):
        for i in range(len(self.rects)):
            screen.blit(self.surfaces[i], self.rects[i])

def main():
    current_level = 0
    player = Player((width / 2, height / 2))
    if COMPILING:
        level = Level(resource_path("img/" + level_file_dict[levellist[current_level]]), player)
    else:
        level = Level(level_file_dict[levellist[current_level]], player)

    pygame.mixer.music.play(-1)

    #Game loop
    while True:
        #deltatime and stable Fps
        dt = clock.tick(60) / 1000
        #event_check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        #blank screen
        screen.fill("#00FFFF")

        #drawing and updating
        level.draw(dt)
        adding = player.update(dt, level)
        if adding:
            if current_level + adding == 6:
                player.the_end()
            elif current_level + adding >= 6:
                current_level = 3
            else:
                current_level += adding
            if COMPILING:
                level = Level(resource_path("img/" + level_file_dict[levellist[current_level]]), player)
            else:
                level = Level(level_file_dict[levellist[current_level]], player)

        
        #screen refresh
        pygame.display.flip()

def interact_entity(entity: Enemy, player: Player, level: Level):
    stop = False
    player.direction_x = 0
    while True:
        mousepos = pygame.mouse.get_pos()
        dt = clock.tick(60) / 1000
        #event_check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if pygame.mouse.get_pressed(5)[0]:
            if mousepos[0] <= width / 2:
                entity.likeing = 1
            else:
                entity.likeing = -1
            stop = True
        
        screen.fill("#00FFFF")
        level.draw(dt)
        screen.blit(textbox, textboxrect.topleft)

        x = arrow_coords[0] - mousepos[0]
        y = arrow_coords[1] - mousepos[1]
        angle = math.degrees(math.atan2(x,y))
        arrow_blit = pygame.transform.rotate(arrow, angle + 180)
        arrow_rect = arrow_blit.get_rect()
        arrow_rect.center = arrow_coords
        screen.blit(arrow_blit, (arrow_rect.x - 16, arrow_rect.y))
        
        if mousepos[0] <= width / 2:
            good_list[1].draw()
            bad_list[0].draw()
        else:
            good_list[0].draw()
            bad_list[1].draw()
        if abs(entity.likeing) >= 1:
            entity.defeated = True
            stop = True

        player.draw((player.direction_x, player.direction_y), dt)
        pygame.display.update()
        
        if stop:
            if abs(entity.likeing) >= 1:
                return True if entity.likeing == -1 else False
            return None
        
def Endscreen(beaten, not_beaten):
    bad_endtexts = []
    good_endtexts = []
    for _ in range(beaten):
        bad_endtexts.append(random.choice(names) + " " + random.choice(endings_bad))
    for _ in range(not_beaten):
        good_endtexts.append(random.choice(names) + " " + random.choice(endings_good))

    y = height / 1
    texts = []

    for text in bad_endtexts + good_endtexts:
        texts.append(Text(text + ".", (width / 2, y), 0.7, "#FFFFFF"))
        y = texts[-1].rects[-1].bottom + 20

    texts.append(Text("Alles in diesem Spiel wurde von Janosch gemacht mit hilfe von Hannes und C", (width / 2, y + 100), 1, "#FFFFFF"))

    while True:
        clock.tick(60)
        screen.fill("#000000")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for text in texts:
            text.draw()
            for rect in text.rects:
                rect.y -= 1
            if texts[-1].rects[-1].y <= 0:
                pygame.quit()
                sys.exit()
        pygame.display.flip()

#initial setup
pygame.init()
pygame.mixer.init()
width, height = 1280, 800
screen = pygame.display.set_mode((width, height))
# defining spritesheets, imgs, fonts and current path
if COMPILING:
    print(resource_path("img/jump_and_run.mp3"))
    print(resource_path("img/character_walk.png"))

    try:
        path = sys._MEIPASS
    except Exception:
        path = os.path.abspath(".")
    player_walk = SpriteSheet(resource_path("img/character_walk.png"))
    player_idle = SpriteSheet(resource_path("img/character_idle.png"))
    npc_idle = SpriteSheet(resource_path("img/npc_idle.png"))
    font = pygame.Font(resource_path("img/prstartk.ttf"))
    textbox = pygame.image.load(resource_path("img/Textbox.png"))
    arrow = pygame.image.load(resource_path("img/arrow.png"))
    pygame.mixer.music.load(resource_path("img/jump_and_run.mp3"))
else:
    path = os.path.abspath(os.path.dirname(__file__))
    player_walk = SpriteSheet(os.path.join(path + "/img/character_walk.png"))
    player_idle = SpriteSheet(os.path.join(path + "/img/character_idle.png"))
    npc_idle = SpriteSheet(os.path.join(path + "/img/npc_idle.png"))
    textbox = pygame.image.load(os.path.join(path + "/img/Textbox.png"))
    arrow = pygame.image.load(os.path.join(path + "/img/arrow.png"))
    font = pygame.Font(os.path.join(path + "/img/prstartk.ttf"))
    pygame.mixer.music.load(os.path.join(path + "/img/jump_and_run.mp3"))

textbox = pygame.transform.scale_by(textbox, 16)
textboxrect = pygame.rect.Rect(width / 2 - textbox.get_width() / 2, height / 2 - textbox.get_height() / 2, textbox.get_width() ,textbox.get_height())
good_text_coords = (textboxrect.centerx - 150, textboxrect.centery - 30)
bad_text_coords = (textboxrect.centerx + 150, textboxrect.centery - 30)
arrow_coords = (textboxrect.centerx, textboxrect.centery + 64)

good_text = Text("sein freund sein", good_text_coords, 0.7, "#000000", 7)
good_text_select = Text("sein freund sein", good_text_coords, 1, "#00AA00", 7)
bad_text = Text("ihn mobben", bad_text_coords, 0.7, "#000000", 7)
bad_text_select = Text("ihn mobben", bad_text_coords, 1, "#FF0000", 7)

good_list = [good_text, good_text_select]
bad_list = [bad_text, bad_text_select]

clock = pygame.time.Clock()

level_file_dict = {
    "tutorial": "lvl_1.tmx",
    "level_2": "lvl_2.tmx",
    "level_3": "lvl_3.tmx",
    "level_4": "school_floor.tmx",
    "level_5": "classroom_1.tmx",
    "level_6": "classroom_2.tmx"
}
names = ["Elias","Liam","Hannes",
"Emilia","Hannah","Sebastian",
"Emma","Julian","Nicole",
"Jonas","Lukas","David",
"Fabian","Sofia","Matteo",
"Jakob","Emil","Leon",
"Daniel","Thomas","Alexander",
"Paul","Felix","Milo",
"Moritz","Samuel","Luise",
"Antonia","Michael","Marcel",
"Anton","Theo","Ben",
"Valentin","Simon","Finn",
"Maximilian","Peter","Adrian",
"Tim","Christian","Kevin",
"Jan","Florian","Kilian",
"Louis","Maxi","Jonathan",
"Julia","Anne","Andreas"]

endings_good = ["mag dich", "ist dein/e Freund/in", "ist immer für dich da", "schenkt dir 10€", "teilt mittagessen"]
endings_bad = ["hat Depression", "weint zuhause", "will Rache nehmen", "will dir aus dem Weg gehen", "hat Suizidgedanken"]

levellist = ["tutorial", "level_2", "level_3", "level_4", "level_5", "level_6"]

player_walk_imgs = []
for y in range(4):
    player_walk_imgs += player_walk.load_strip((0,32 * y, 32, 32), 4)

player_idle_img = []
for y in range(2):
    player_idle_img += player_idle.load_strip((0,32 * y, 32, 32), 6)

npc_idle_img = []
for y in range(2):
    npc_idle_img += npc_idle.load_strip((0,32 * y, 32, 32), 6)

