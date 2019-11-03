import pygame
from classes.tile import Tile


class Button(Tile):
    def __init__(self, pos, tile):
        super().__init__(pos, tile, collision=False)
        self.width, self.height = 7, 10
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((0, 255, 0))
        self.pressed = False

        if tile == 3.01:
            self.looking_right = True
        if tile == 3.02:
            self.looking_right = False
        if tile == 3.03:
            self.looking_right = False

    def collide_player(self, player):
        if self.get_rect().colliderect(player.get_rect()):
            return True
        return False

    def get_rect(self):
        return pygame.Rect(self.x, self.y, Tile.width, Tile.height)

    def was_pressed(self):
        self.width /= 2
        self.pressed = True

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((0, 255, 0))

    def was_unpressed(self):
        self.width *= 2
        self.pressed = False

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((0, 255, 0))

    def draw(self, surface):
        x_offset = 0
        y_offset = 15
        if not self.looking_right:
            x_offset += 64 - self.width

        if self.pressed and self.looking_right:
            self.width -= self.width/2

        surface.blit(self.surface, (self.x + x_offset, self.y + y_offset))