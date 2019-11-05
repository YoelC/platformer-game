import pygame
from classes.tile import Tile


class Button(Tile):
    closed_img = pygame.image.load('images/button/closed.png')
    closed_img = pygame.transform.scale(closed_img, (closed_img.get_rect().width*2, closed_img.get_rect().height*2)).convert_alpha()
    open_img = pygame.image.load('images/button/opened.png')
    open_img = pygame.transform.scale(open_img, (open_img.get_rect().width*2, open_img.get_rect().height*2)).convert_alpha()

    def __init__(self, pos, tile):
        super().__init__(pos, tile, collision=False)
        self.width, self.height = 7, 10
        self.img = self.closed_img
        self.pressed = False

    def collide_player(self, player):
        if self.get_rect().colliderect(player.get_rect()):
            return True
        return False

    def get_rect(self):
        return pygame.Rect(self.x, self.y, Tile.width, Tile.height)

    def was_pressed(self):
        self.width /= 2
        self.pressed = True

        self.img = self.open_img

    def was_unpressed(self):
        self.width *= 2
        self.pressed = False

        self.img = self.closed_img

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((0, 255, 0))

    def draw(self, surface):
        x_offset = -15
        y_offset = 7

        surface.blit(self.img, (self.x + x_offset, self.y + y_offset))