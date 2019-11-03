import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT
from math import sqrt


class Camera:
    def __init__(self, player):
        self.width, self.height = WINDOW_WIDTH, WINDOW_HEIGHT
        self.x, self.y = 0, 0
        self.x_vel, self.y_vel = 0, 0
        self.objects = []

        self.x_zone = self.width / 2 - 100
        self.y_zone = self.height / 2 - 75

        self.player = player
        self.objects.append(self.player)

        self.top_black_bar = BlackBar(is_top=True)
        self.bottom_black_bar = BlackBar(is_top=False)

    def set_pos(self, pos):
        x = self.x - pos[0]
        y = self.y - pos[1]
        for item in self.objects:
            item.x += x
            item.y -= y
        self.x = pos[0]
        self.y = pos[1]

        self.player.center()

    def move_delta(self, delta):
        for item in self.objects:
            item.x -= delta[0]
            item.y += delta[1]

        self.x += delta[0]
        self.y += delta[1]

    def set_black_bars(self, black_bars):
        if black_bars:
            self.bottom_black_bar.set_pos(WINDOW_HEIGHT - 96)
            self.top_black_bar.set_pos(96 - BlackBar.height)
        elif not black_bars:
            self.bottom_black_bar.set_pos(WINDOW_HEIGHT)
            self.top_black_bar.set_pos(-BlackBar.height)

    def cap_vel(self, vel):
        x_vel, y_vel = vel
        if x_vel is not None:
            if abs(self.x_vel) > x_vel:
                self.x_vel = x_vel if self.x_vel > 0 else -x_vel

        if y_vel is not None:
            if abs(self.y_vel) > y_vel:
                self.y_vel = y_vel if self.y_vel > 0 else -y_vel

    def move(self, player):
        self.x_zone = self.width / 2 - 100
        self.y_zone = self.height / 2 - 75

        player_x = player.x + player.width / 2
        player_y = player.y + player.height / 2

        # Right deadzone
        if player_x > self.width - self.x_zone:
            self.x_vel = player.x_vel
        elif player_x < self.width - self.x_zone and self.x_vel > 0:
            self.x_vel *= 0.8

        # Left deadzone
        if player_x < self.x_zone:
            self.x_vel = player.x_vel
        elif player_x > self.x_zone and self.x_vel < 0:
            self.x_vel *= 0.8

        # Top deadzone
        if player_y > self.height - self.y_zone - 50:
            self.y_vel = -player.y_vel
        elif player_y < self.height - self.y_zone - 50 and self.y_vel < 0:
            self.y_vel *= 0.8

        # Bottom deadzone
        if player_y < self.y_zone - 50:
            self.y_vel = -player.y_vel
        elif player_y > self.y_zone - 50 and self.y_vel > 0:
            self.y_vel *= 0.8

        self.cap_vel((15, None))
        self.move_delta((self.x_vel, self.y_vel))

        self.top_black_bar.move()
        self.bottom_black_bar.move()

    def add_object(self, item):
        self.objects.append(item)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), (self.x_zone, self.y_zone - 50, 200, 150), 2)

    def draw_black_bar(self, surface):
        self.top_black_bar.draw(surface)
        self.bottom_black_bar.draw(surface)


class BlackBar:
    height = WINDOW_HEIGHT / 8
    width = WINDOW_WIDTH

    def __init__(self, is_top):
        self.x = 0
        self.y = WINDOW_HEIGHT
        self.x_vel, self.y_vel = 0, 0

        self.is_top = is_top

        self.on_screen = False
        if is_top:
            self.y = -self.height

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((0, 0, 0))

    def move(self):
        self.y_vel = round(self.y_vel, 1)
        self.x_vel = round(self.x_vel, 1)

        self.x += self.x_vel
        self.y -= self.y_vel

        self.x_vel -= 0

        self.y_vel = round(self.y_vel, 1)
        self.x_vel = round(self.x_vel, 1)

        print(self.y_vel)

    def set_pos(self, wish_pos):
        dy = self.y - wish_pos
        vf = 0
        t = 15
        self.y_vel = round((-(vf * t) + (2 * dy))/t, 1)

    def draw(self, surface):
        surface.blit(self.surface, (self.x, self.y))

