import pygame
import math
import sys
import os

pygame.init()

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

COMPILING = False

pygame.init()
width, height = 1280,800
screen = pygame.display.set_mode((width, height))
HOME = 0
ON_THE_WAY = 1
SCHOOL = 2
SCHOOLHALL = 3
CLASSROOM = 4
CAFETERIA = 5

if not COMPILING:
    path = os.path.abspath(os.path.dirname(__file__))
    font = pygame.Font(os.path.join(path + "/img/prstartk.ttf"))
    arrow = pygame.image.load(os.path.join(path + "/img/arrow.png"))
    overlay = pygame.image.load(os.path.join(path + "/img/handy_overlay.png"))
else:
    font = pygame.Font(resource_path("img/prstartk.ttf"))
    arrow = pygame.image.load(resource_path("img/arrow.png"))
    overlay = pygame.image.load(resource_path("img/handy_overlay.png"))
arrow_coords = (width / 2,height / 2)

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
            texts.append(text[old_space:space].strip())
            old_space = space
            
    texts.append(text[old_space:])
    return texts

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

def read_table_at(table, colum, row):
    return table[colum][row]

def Endscreen(rep, overlay):
    end_text = Text(f"du {"wurdest unbeliebter" if rep < 100 else "wurdest nicht unbeliebter"}", (width / 2, height / 2), 1)
    time_text = Text(str(17)+":00", (85,45), 0.75)
    rep_text = Text("♥:"+str(rep), (width - 85,45), 0.75)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill("#00FFFF")
        screen.blit(overlay, (0,0))
        end_text.draw()
        time_text.draw()
        rep_text.draw()
        pygame.display.flip()


def main(overlay = overlay):
    time = 0
    place = HOME
    clock = pygame.Clock()
    overlay = pygame.transform.scale(overlay, (width, height))
    time_text = Text(str(time + 6)+":00", (85,45), 0.75)
    rep = 100
    rep_text = Text("♥:"+str(rep), (width - 85,45), 0.75)
    #--------------------------------------------------TABLE--------------------------------------------------
    table_of_contend = []
    for i in range(6):
        table_of_contend.append([])
        for j in range (12):
            table_of_contend[i].append(["EmptyQ", "EmptyA1", "EmptyA2"])
    for i in range(12):
        table_of_contend[HOME][i] = "Du bist Zuhause und du schaust oben links auf die Zeit", "stehst du auf und gehst zur schule", "Du schläfst weiter"
    table_of_contend[HOME][0] = "Du bist Zuhause und du schaust oben links auf die Zeit und dein Wecker klingelt.", "steh auf und geh zur schule", "schlaf weiter"
    table_of_contend[HOME][6] = "Du bist Zuhause und es ist schon 12:00", "steh auf und geh zur schule", "schlaf weiter"
    for i in range(10):
        table_of_contend[ON_THE_WAY][i + 1] = ("Du bist auf dem Weg zur Schule, etwas spät, aber du schaffst es aber noch rechtzeitig", "geh zur Schule", "geh wieder nach Hause")
    table_of_contend[ON_THE_WAY][1] = ("Du bist auf dem Weg zur Schule, als du deinen Mobber vor der Schule siehst", "versuch unbemerkt an ihm vorbei zu gehen", "geh nach Hause")
    for i in range(9):
        table_of_contend[SCHOOL][i + 2] = ("Vor Der Schule", "Geh in die      Schule", "Warte vor der   Schule")
    for i in range(8):
        if i % 2 == 0:
            table_of_contend[SCHOOLHALL][i + 3] = ("Auf dem Schulgang", "Geh zur Unterrichts-  stunde", "Rede mit deinem Freund den sonst niemand mag")
        else:
            table_of_contend[SCHOOLHALL][i + 3] = ("Auf dem Schulgang", "Geh zur Unterrichts-  stunde", "Warte auf dem Klo")
    for i in range(7):
        table_of_contend[CLASSROOM][i + 4] = ("Im Klassenzimmer", "Beteiligst du   dich aktiv  an der Unterrichts- stunde und geh essen", "Schlaf im Unterricht")
    for i in range(6):
        table_of_contend[CAFETERIA][i + 5] = ("In der Cafeteria", "Iss nichts und geh richtung Schulgang","Iss etwas")

    question = Question(table_of_contend, place, time)
    #--------------------------------------------------MAIN_LOOP--------------------------------------------------

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.fill("#00FFFF")
        screen.blit(overlay, (0,0))
        result = question.update()
        if result != 0:
            rep += 1 if result == 1 else -1
            time += 1
            time_text = Text(str(time + 6)+":00", (85,45), 0.75)
            rep_text = Text("♥:"+str(rep), (width - 85,45), 0.75)

            if result == 2:
                place -= 1 if place < SCHOOL else 0
            else:
                place += 1 if result == 1 else -1
            place = max(place, 0)
            if time == 3 and place == HOME:
                time = 6
                time_text = Text(str(time + 6)+":00", (85,45), 0.75)
            if place > CAFETERIA:
                place = SCHOOLHALL
            if time == 11:
                Endscreen(rep, overlay)
            question.update_table(place, time)
        time_text.draw()
        rep_text.draw()
        pygame.display.flip()

#--------------------------------CLASSES_CLASSES_CLASSES--------------------------------
#--------------------------------CLASSES_CLASSES_CLASSES--------------------------------
#--------------------------------CLASSES_CLASSES_CLASSES--------------------------------

class Text:
    
    def __init__(self, text: str, pos: tuple, scale, color = "#000000", breakpoint = 10):
        
        last_height = 0
        self.rects = []
        self.surfaces = []
        texts = sep_text(text, breakpoint)
        
        for i,string in enumerate(texts):
            surface = font.render(string, False, color)
            surface = pygame.transform.scale_by(surface, scale)
            rect = surface.get_rect()
            rect.centerx = pos[0]
            rect.top = pos[1] + last_height + 10
            last_height = rect.bottom - pos[1]
            self.surfaces.append(surface)
            self.rects.append(rect)
        
    def draw(self):
        for i in range(len(self.rects)):
            screen.blit(self.surfaces[i], self.rects[i])

class Question:
    def __init__(self, table, start_colum, start_row):
        self.table = table
        self.colum = start_colum
        self.row = start_row
        self.load_questions()
        self.load_text()
        self.last = 0

    def draw(self):
        for i in range(3):
            self.texts[i].draw()

    def update_table(self, colum, row, table = None):
        self.table = table if table is not None else self.table
        self.colum = colum
        self.row = row
        self.load_questions()
        self.load_text()

    def load_questions(self):
        self.strings = read_table_at(self.table, self.colum, self.row)
        if self.strings == ["EmptyQ", "EmptyA1", "EmptyA2"]:
            print(f"Error occured at colum: {self.colum} and row: {self.row}")
        self.question = self.strings[0]
        self.answera = self.strings[1]
        self.answerb = self.strings[2]

    def load_text(self):
        self.texts = []
        self.texts.append(Text(self.question, (width / 2,height / 2 - 300), 1, "#000000", 15))
        self.texts.append(Text(self.answera, (width / 2 - 300,height / 2), 1, "#000000", 15))
        self.texts.append(Text(self.answerb, (width / 2 + 300,height / 2), 1, "#000000", 15))


    def update(self):
        mousepos = pygame.mouse.get_pos()
        x = arrow_coords[0] - mousepos[0]
        y = arrow_coords[1] - mousepos[1]
        angle = math.degrees(math.atan2(x,y))
        arrow_blit = pygame.transform.rotate(arrow, angle + 180)
        arrow_rect = arrow_blit.get_rect()
        arrow_rect.center = arrow_coords
        screen.blit(arrow_blit, (arrow_rect.x - 16, arrow_rect.y))
        self.draw()
        if pygame.mouse.get_pressed()[0]:
            self.last = 1
        else:
            if self.last == 1:
                self.last = 0
                return 1 if mousepos[0] <= width / 2 else 2
            self.last = 0
        return 0
