import pygame, sys, os
import opfer
import taeter

pygame.init()

Compiling = False

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
if not Compiling:
    path = os.path.abspath(os.path.dirname(__file__))
    font = pygame.Font(os.path.join(path + "/img/prstartk.ttf"))
else:
    font = pygame.Font(resource_path("img/prstartk.ttf"))
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
            rect.centery = pos[1] + last_height + 15
            last_height = rect.height * (i + 1)
            self.surfaces.append(surface)
            self.rects.append(rect)
        
    def draw(self):
        for i in range(len(self.rects)):
            screen.blit(self.surfaces[i], self.rects[i])
screen = pygame.display.set_mode((1280,800))
width, height = 1280, 800
taeter_text = Text("Täter", (width / 2 + width / 4, height / 2), 1, "#FFFFFF")
opfer_text = Text("Opfer", (width / 4, height / 2), 1, "#FFFFFF")
def main():
    last = 0
    while True:
        screen.fill("#000000")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if pygame.mouse.get_pressed()[0]:
                last = 1
        else:
            if last == 1:
                last = 0
                if pygame.mouse.get_pos()[0] <= 1280 / 2:
                    opfer.main()
                else:
                    taeter.main()
            last = 0
        taeter_text.draw()
        opfer_text.draw()
        pygame.display.flip()

if __name__ == "__main__":
    main()