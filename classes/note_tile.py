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

        self.text = f'Debug text ({tile})'
        if tile == 5.01:
            self.text = "This is the test room. There are a few features that are still being tested here. Please notice that the textures (and most stuff as well!) will not look like here."
        if tile == 5.02:
            self.text = "Any feedback or bug reporting would be appreciated on my github: github.com/YoelC/ platformer-game"
            self.looking_right = True

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 64, 64)

    def draw(self, surface):
        x_offset = 0
        if self.looking_right:
            x_offset += 64 - self.width

        surface.blit(self.surface, (self.x + x_offset, self.y))
