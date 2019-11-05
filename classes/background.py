import pygame


class Background:
    # Test
    img = pygame.image.load('images/environment/room1.png').convert_alpha()
    img = pygame.transform.scale(img, (img.get_rect().width * 2, img.get_rect().height * 2)).convert_alpha()

    def __init__(self):
        self.x, self.y = 384, 192
        self.width, self.height = self.img.get_rect().width, self.img.get_rect().height

    def draw(self, surface):
        surface.blit(self.img, (self.x, self.y))
