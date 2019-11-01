import pygame


class Tile:
    width, height = 64, 64

    def __init__(self, pos):
        self.x, self.y = pos[0] * self.width, pos[1] * self.height
        self.x_vel, self.y_vel = 0, 0

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((255, 0, 0))

    def get_rect(self):
        return pygame.Rect((self.x, self.y, self.width, self.height))

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def draw(self, surface):
        surface.blit(self.surface, (self.x, self.y))