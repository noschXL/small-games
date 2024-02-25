import pygame,sys,time

pygame.init()

wn = pygame.display.set_mode((600,600))

feld_breite = feld_höhe = 200

_WHITE = pygame.Color(255,255,255)
_BLACK = pygame.Color(0,0,0)
_RED = pygame.Color(255,0,0)

class feld:
    felder = []
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.pos = (x / feld_breite + 1) + (y / feld_höhe * 3)
        self.status = None
        self.rect = pygame.rect.Rect(x, y, feld_breite, feld_höhe)

    def draw(self):
        pygame.draw.rect(wn, _WHITE, self.rect)
        if self.status == 1:
            pygame.draw.line(wn, _BLACK,(self.x + 20, self.y + 20),(self.x + feld_breite - 20, self.y + feld_höhe - 20), 5)
            pygame.draw.line(wn, _BLACK,(self.x + 20, self.y + 180),(self.x + feld_breite- 20, self.y + 20), 5)
        elif self.status == 2:
            pygame.draw.circle(wn, _BLACK, (self.x + 100, self.y + 100), 90)
            pygame.draw.circle(wn, _WHITE, (self.x + 100, self.y + 100), 85)

    def get_pos(self):
        return self.pos

    def get_status(self):
        return self.status
    
    def set_status(self, new_status):
        self.status = new_status

    def get_xy(self):
        return self.x,self.y
        
for y in range (3):
    for x in range(3):
        feld.felder.append(feld(x * feld_breite, y * feld_höhe))

spieler = 1
pygame.display.set_caption("TicTacToe")
'''
def win():
    fs = feld.felder
    lines = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]
    for line in lines:
        f1 = line[0]
        f2 = line[1]
        f3 = line[2]
        if fs[f1].get_status() == None:
            continue

        if fs[f1].get_status() == fs[f2].get_status() == fs[f3].get_status():
            pygame.display.set_caption(f"spieler {spieler} hat gewonnen")
            xy_f1 = fs[f1].get_xy()
            xy_f3 = fs[f3].get_xy()
            pygame.draw.line(wn, _RED,(xy_f1),(xy_f3[0] + feld_breite, xy_f3[1] + feld_höhe))
'''
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        buttons = pygame.mouse.get_pressed(5)
        if buttons[0]:
            mousepos = pygame.mouse.get_pos()
            xpos = mousepos[0] // 200 + 1
            ypos = mousepos[1] // 200 * 3
            pos = xpos + ypos
            for f in feld.felder:
                if f.get_pos() == pos:
                    if f.get_status() == None:
                        f.set_status(spieler)
                        spieler = 1 if spieler == 2 else 2


    for f in feld.felder:
        f.draw()

    for y in range(2):
        for x in range(2):
            pygame.draw.line(wn, _BLACK,(x * 200 + 200, y),(x * 200 + 200, 600), 7)
        pygame.draw.line(wn, _BLACK,(x, y * 200 + 200),(600, y * 200 + 200), 7)

    fs = feld.felder
    lines = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]
    for line in lines:
        f1 = line[0]
        f2 = line[1]
        f3 = line[2]
        if fs[f1].get_status() == None:
            continue

        if fs[f1].get_status() == fs[f2].get_status() == fs[f3].get_status():
            pygame.display.set_caption(f"spieler {spieler} hat gewonnen")
            #xy_f1 = fs[f1].get_xy()
            #xy_f3 = fs[f3].get_xy()
            #pygame.draw.line(wn, _RED,(xy_f1),(xy_f3[0] + feld_breite, xy_f3[1] + feld_höhe),10)

    pygame.display.flip()

