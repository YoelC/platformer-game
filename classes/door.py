import pygame
from classes.tile import Tile


class Door(Tile):
    def __init__(self, pos, tile):
        super().__init__(pos, tile, collision=False)
        self.pressed = False
        self.width, self.height = 42, 64
        self.y -= 8
        self.height += 8
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((120, 70, 20))

        # 22

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 64, 64)

    def draw(self, surface):
        surface.blit(self.surface, (self.x + 11, self.y))
