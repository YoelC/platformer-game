import pygame
from random import randint


class Background:
    star_count = 150

    def __init__(self):
        self.stars = []
        self.x, self.y = 0, 0
        for i in range(self.star_count):
            self.stars.append(Star((randint(0, 1280), randint(0, 768), randint(1, 5))))


class Star:
    def __init__(self, pos):
        self.x, self.y = pos[:2]
        self.width, self.height = pos[2] * 10
        self.x_vel, self.y_vel = 0, 0

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def draw(self):
        pass