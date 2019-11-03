import pygame
from classes.tile import Tile


class NoteTile(Tile):
    def __init__(self, pos, tile):
        super().__init__(pos, tile, collision=False)
        self.width, self.height = 7, 30
        self.looking_right = False
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((255, 251, 191))
        self.reading = False

        self.text = 'There is no text here.'

        if tile == 5.02:
            self.looking_right = True

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 64, 64)

    def draw(self, surface):
        x_offset = 0
        if self.looking_right:
            x_offset += 64 - self.width

        surface.blit(self.surface, (self.x + x_offset, self.y))
