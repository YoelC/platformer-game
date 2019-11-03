import pygame


class Camera:
    def __init__(self, size):
        self.width, self.height = size
        self.x, self.y = 0, 0
        self.x_vel, self.y_vel = 0, 0
        self.objects = []

        self.x_zone = self.width / 2 - 100
        self.y_zone = self.height / 2 - 75

    def set_pos(self, pos):
        for item in self.objects:
            item.x += pos[0]
            item.y -= pos[1]
        self.x = pos[0]
        self.y = pos[1]

    def move_delta(self, delta):
        for item in self.objects:
            item.x -= delta[0]
            item.y += delta[1]

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

    def add_object(self, item):
        self.objects.append(item)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), (self.x_zone, self.y_zone - 50, 200, 150), 2)
