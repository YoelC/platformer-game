from classes.tile import Tile
import pygame


class WaterTile(Tile):
    def __init__(self, pos, tile):
        super().__init__(pos, tile, collision=False)
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.surface.fill((0, 255, 255, 64))

    def get_rect(self):
        return pygame.Rect(self.x, self.y + self.height/2,self.width, self.height/2)