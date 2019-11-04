import pygame


class Tile:
    width, height = 64, 64

    def __init__(self, pos, tile, collision=True, height=64):
        self.x, self.y = pos[0] * self.width, pos[1] * self.height
        self.x_vel, self.y_vel = 0, 0
        self.tile = tile

        self.walljump = False
        self.collision = collision
        self.activated = True
        self.height = height

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((255, 0, 0))

        if tile == 2:
            self.surface.fill((0, 0, 255))
            self.walljump = True

        if tile == 1.5:
            self.walljump = False

    def get_rect(self):
        return pygame.Rect((self.x, self.y, self.width, self.height))

    def collide_player(self, player):
        # X collision
        if self.activated:
            inside_any = False
            touching_left, touching_right = False, False
            temp_x_rect = pygame.Rect(player.x + player.x_vel - self.x_vel, player.y, player.width, player.height)
            if temp_x_rect.colliderect(self.get_rect()):
                inside_any = True
                if self.collision:
                    if player.x_vel - self.x_vel > 0:
                        player.x = self.x - player.width
                        player.x_vel = self.x_vel
                        touching_left = True

                    else:
                        player.x = self.x + self.width
                        player.x_vel = self.x_vel
                        touching_right = True

            # Y Collision
            on_surface = False
            temp_y_rect = pygame.Rect(player.x, player.y + player.y_vel - self.y_vel, player.width, player.height)
            if temp_y_rect.colliderect(self.get_rect()):
                inside_any = True
                if self.collision:
                    if player.y_vel - self.y_vel > 0:
                        player.y = self.y - player.height
                        player.y_vel = self.y_vel
                        on_surface = True

                    else:
                        player.y = self.y + self.height
                        player.y_vel = self.y_vel

            # Checking for rwall, lwall collision
            if self.collision:
                temp_rwall_rect = pygame.Rect(player.x + 1 - self.x_vel, player.y, player.width, player.height)
                if temp_rwall_rect.colliderect(self.get_rect()):
                    touching_left = True
                temp_lwall_rect = temp_rwall_rect.copy()
                temp_lwall_rect.x -= 2
                if temp_lwall_rect.colliderect(self.get_rect()):
                    touching_right = True

            if self.walljump:
                return on_surface, touching_right, touching_left, inside_any
            if not self.walljump:
                return on_surface, False, False, inside_any
        return False, False, False, False

    def activate(self):
        self.activated = False

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def draw(self, surface):
        if self.activated:
            surface.blit(self.surface, (self.x, self.y))
