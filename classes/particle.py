import pygame


class Particle:
    def __init__(self, pos, vel, color, lifetime, gravity=True):
        self.x, self.y, self.width = pos
        self.height = self.width

        self.x_vel, self.y_vel = vel
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA).convert_alpha()
        self.color = color
        self.surface.fill(self.color)

        self.lifetime = 255
        self.lifetime_rate = lifetime

        self.gravity = True

        self.dead = False

    def move(self):
        if self.gravity:
            self.y_vel += 1

        self.x += self.x_vel
        self.y += self.y_vel

        self.lifetime -= self.lifetime_rate

    def draw(self, surface):
        if self.lifetime < 0:
            self.surface.fill((0, 0, 0, 0))
            self.dead = True
        else:
            self.surface.fill((self.color[0], self.color[1], self.color[2], self.lifetime))

        surface.blit(self.surface, (self.x, self.y))
