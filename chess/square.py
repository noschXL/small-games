# square class

import pygame 
wn = pygame.display 
class squares:
    fields = []

    def __init__(self, x, y, colorblack, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.piece = None
        if colorblack:
            self.color = pygame.Color(93, 50, 49)  # Color for black squares
        else:
            self.color = pygame.Color(121, 72, 57, 255)  # Color for white squares
        self.originalcolor = self.color

    def draw(self):
        pygame.draw.rect(wn, self.color, (self.x * 80, self.y * 80, self.width, self.height))
        if self.piece is not None:
            wn.blit(self.piece.get_sprite(), (self.x * 80 + 5, self.y * 80 + 5))  # Offset the pawn sprite position

    def get_xy(self):
        return self.x, self.y

    def get_pos(self):
        return self.y * 8 + self.x

    def get_piece(self):
        return self.piece

    def set_piece(self, piece):
        self.piece = piece

    def set_color(self,color):
        self.oldcolor = self.color
        self.color = color

    def reset_color(self):
        self.color = self.originalcolor