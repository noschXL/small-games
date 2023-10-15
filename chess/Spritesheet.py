# spritesheet class
import os
import pygame

pygame.display.set_mode((0,0))

pathdir = os.path.dirname(os.path.abspath(__file__))

class SpriteSheet:

    def __init__(self, filename):
        """Load the sheet."""
        self.spritepath = os.path.join(pathdir,'img',filename)
        try:
            self.sheet = pygame.image.load(self.spritepath).convert()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)


    def image_at(self, rectangle, colorkey = None):
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
