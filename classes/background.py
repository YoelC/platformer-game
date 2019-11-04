import pygame


class Background:
    # Test
    img = pygame.Surface((15, 15))
    img = pygame.transform.scale(img, (img.get_rect().width, img.get_rect().height))

    def __init__(self):
        self.x, self.y = 0, 0
        self.width, self.height = self.img.get_rect().width, self.img.get_rect().height

    def draw(self, surface):
        surface.blit(self.img, (self.x, self.y))
