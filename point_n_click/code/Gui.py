import pygame

class Button():
    def __init__(self, screen: pygame.Surface,pos: tuple[int], label: str, font: pygame.Font,center: bool = True, bg: str = "#000000", hoverbg: str = "#FFFFFF", text_color: str = "#FFFFFF", hover_text_color: str = "#000000", rounded = -1,text_size = 1):

        self.screen = screen
        self.center = center

        self.label = label
        self.font = font
        self.textsize = text_size

        self.hoverd = False

        self.bg = bg
        self.hoverbg = hoverbg
        self.rounded = rounded

        self.textcolor = text_color
        self.hovertextcolor = hover_text_color

        surf = font.render(self.label, True, self.textcolor, self.bg)
        self.rect = surf.get_rect()
        if self.center:
            self.rect.center = pos
        else: self.rect.topleft = pos
        self.final_surf = pygame.Surface((self.rect.width + 2, self.rect.height + 2))
        pygame.draw.rect(self.final_surf, "#000000", (0,0,self.rect.width + 2, self.rect.height + 2), 1, rounded, rounded, rounded, rounded, rounded)
        self.final_surf.blit(surf, (1,1))

        surf = font.render(self.label, True, self.hovertextcolor, self.hoverbg)
        self.hover_final_surf = pygame.Surface((self.rect.width + 2, self.rect.height + 2))
        pygame.draw.rect(self.hover_final_surf, "#000000", (0,0,self.rect.width + 2, self.rect.height + 2), 1, rounded, rounded, rounded, rounded, rounded)
        self.hover_final_surf.blit(surf, (1,1))

    def draw(self):
        if self.hoverd:
            self.screen.blit(self.final_surf, (self.rect.x + 1, self.rect.y + 1))
        else:
            self.screen.blit(self.hover_final_surf, (self.rect.x + 1, self.rect.y + 1))

    def update(self, mousepos):
        rect = pygame.Rect(mousepos[0], mousepos[1], 1, 1)
        if self.rect.colliderect(rect):
            self.hoverd = True
        else:
            self.hoverd = False


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


class Text:
    
    def __init__(self, text: str, font: pygame.Font,screen: pygame.Surface ,pos: tuple, scale, color = "#000000", breakpoint = 10, line_spacing = 5):
        
        last_height = 0
        self.screen = screen
        self.rects = []
        self.surfaces = []
        texts = sep_text(text, breakpoint)
        
        for string in texts:
            surface = font.render(string, False, color)
            surface = pygame.transform.scale_by(surface, scale)
            rect = surface.get_rect()
            rect.centerx = pos[0]
            rect.top = pos[1] + last_height + line_spacing
            last_height = rect.bottom - pos[1]
            self.surfaces.append(surface)
            self.rects.append(rect)
        
    def draw(self):
        for i in range(len(self.rects)):
            self.screen.blit(self.surfaces[i], self.rects[i])