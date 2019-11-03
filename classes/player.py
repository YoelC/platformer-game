import pygame
from config import FONT


class Player:
    width, height = 30, 64
    vel = 1
    max_vel = 15
    jump_vel = 17

    scale = (100, 74)
    air_imgs = [pygame.image.load('images/player/air_cycle/adventurer-fall-00.png'),
                pygame.image.load('images/player/air_cycle/adventurer-fall-01.png')]
    for i, img in enumerate(air_imgs):
        air_imgs[i] = pygame.transform.scale(img, (scale[0] + 13, scale[1] + 5))

    idle_imgs = [pygame.image.load('images/player/idle_cycle/adventurer-idle-00.png'),
                 pygame.image.load('images/player/idle_cycle/adventurer-idle-01.png')]
    for i, img in enumerate(idle_imgs):
        idle_imgs[i] = pygame.transform.scale(img, scale)

    jump_imgs = [pygame.image.load('images/player/jump_cycle/adventurer-jump-00.png'),
                 pygame.image.load('images/player/jump_cycle/adventurer-jump-01.png')]
    for i, img in enumerate(jump_imgs):
        jump_imgs[i] = pygame.transform.scale(img, (scale[0] + 13, scale[1] + 5))

    walk_imgs = [pygame.image.load('images/player/walk_cycle/walk-00.png'),
                 pygame.image.load('images/player/walk_cycle/walk-01.png'),
                 pygame.image.load('images/player/walk_cycle/walk-02.png'),
                 pygame.image.load('images/player/walk_cycle/walk-03.png'),
                 pygame.image.load('images/player/walk_cycle/walk-04.png'),
                 pygame.image.load('images/player/walk_cycle/walk-05.png')]
    for i, img in enumerate(walk_imgs):
        walk_imgs[i] = pygame.transform.scale(img, (scale[0] + 13, scale[1] + 5))

    wall_slide_imgs = [pygame.image.load('images/player/wall_slide_cycle/adventurer-wall-slide-00.png'),
                       pygame.image.load('images/player/wall_slide_cycle/adventurer-wall-slide-01.png')]
    for i, img in enumerate(wall_slide_imgs):
        wall_slide_imgs[i] = pygame.transform.scale(img, scale)

    crouch_imgs = [pygame.image.load('images/player/crouch_cycle/adventurer-crouch-00.png'),
                   pygame.image.load('images/player/crouch_cycle/adventurer-crouch-01.png'),
                   pygame.image.load('images/player/crouch_cycle/adventurer-crouch-02.png'),
                   pygame.image.load('images/player/crouch_cycle/adventurer-crouch-03.png')]
    for i, img in enumerate(crouch_imgs):
        crouch_imgs[i] = pygame.transform.scale(img, scale)

    def __init__(self, pos):
        self.x, self.y = pos
        self.x_vel, self.y_vel = 0, 0

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((255, 255, 255))

        self.moving_left, self.moving_right, self.jumping, self.moving_down = False, False, False, False
        self.on_surface, self.on_rwall, self.on_lwall = False, False, False
        self.img_count = 0
        self.jump_count = 0
        self.looking_right = True
        self.slide_ability = True

        self.attached_text = ''

        self.use = False

    def cap_speed(self):
        if abs(self.x_vel) > abs(self.max_vel):
            self.x_vel = self.max_vel if self.x_vel > 0 else -self.max_vel

        if self.y_vel > 40 and self.moving_down:
            self.y_vel = 40

        if self.y_vel > 20 and not self.moving_down:
            self.y_vel = 20

    def calculate_move(self):
        self.y_vel += 1

        if self.moving_right and self.moving_left or (self.moving_down and self.on_surface):
            self.moving_right, self.moving_left = False, False

        if self.moving_down:
            self.y_vel += 1

        if self.moving_left:
            self.x_vel -= self.vel

        if self.moving_right:
            self.x_vel += self.vel

        if self.jumping and self.on_surface:
            self.y_vel -= self.jump_vel
            self.jump_count = 1

        self.cap_speed()

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def calculate_walljump(self, relative_y_vel):
        self.slide_ability = True

        if self.moving_down:
            self.slide_ability = False

        if self.on_surface:
            self.slide_ability = False

        if self.slide_ability:
            if self.jumping and self.on_lwall and not self.on_surface:
                self.y_vel = -15 * 0.707 + relative_y_vel
                self.x_vel -= 15 * 0.707
                self.jump_count = 1

            if self.jumping and self.on_rwall and not self.on_surface:
                self.y_vel = -15 * 0.707 + relative_y_vel
                self.x_vel += 15 * 0.707
                self.jump_count = 1

            if self.on_rwall or self.on_lwall and not self.on_surface:
                if self.y_vel > 4:
                    self.y_vel = 4

        if self.on_surface and not (self.moving_right or self.moving_left or self.jumping):
            self.x_vel *= 0.75
            if abs(self.x_vel) < 0.1:
                self.x_vel = 0

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset_variables(self):
        self.moving_left, self.moving_right, self.jumping, self.moving_down = False, False, False, False

    def left(self):
        self.moving_left = True

    def right(self):
        self.moving_right = True

    def jump(self):
        self.jumping = True

    def down(self):
        self.moving_down = True

    def draw_text(self, surface):
        # Text drawing
        if self.attached_text != '':
            font_surface, font_pos = FONT.render(self.attached_text, size=25, fgcolor=(255, 255, 255))
            surface.blit(font_surface, (self.x - font_pos.width / 3, self.y - 25))

    def draw(self, surface):
        img = self.surface
        offset_x = -35
        offset_y = -8

        # Falling
        if not self.on_surface:
            self.img_count %= 2
            img = self.air_imgs[int(self.img_count)]
            if self.moving_down:
                self.img_count += 0.4
            else:
                self.img_count += 0.1
            offset_x, offset_y = (-42, -14)

        # Idle Falling
        if not self.on_surface and round(self.x_vel) == 0:
            self.img_count %= 2
            img = self.air_imgs[int(self.img_count)]
            if not self.looking_right:
                img = pygame.transform.flip(img, True, False)
            if self.moving_down:
                self.img_count += 0.2
            else:
                self.img_count += 0.1
            offset_x, offset_y = (-42, -14)

        # Jumping
        if self.jump_count != 0:
            self.jump_count += 0.1
            try:
                img = self.jump_imgs[int(self.jump_count) - 1]
            except IndexError:
                self.jump_count = 0
            offset_x, offset_y = (-42, -14)

        # Idle Jumping
        if self.jump_count != 0 and round(self.x_vel) == 0:
            self.jump_count += 0.1
            if not self.looking_right:
                img = pygame.transform.flip(img, True, False)
            offset_x, offset_y = (-42, -14)

        # Idle
        if not self.moving_down:
            if self.on_surface and round(self.x_vel) == 0:
                self.img_count %= 2
                img = self.idle_imgs[int(self.img_count)]
                if not self.looking_right:
                    img = pygame.transform.flip(img, True, False)
                self.img_count += 0.1
                offset_x, offset_y = (-35, -8)

            # Walking
            elif self.on_surface:
                self.img_count %= 6
                img = self.walk_imgs[int(self.img_count)]
                self.img_count += abs(self.x_vel)/50
                offset_x, offset_y = (-42, -14)

        # Crouching
        elif self.on_surface:
            self.img_count %= 4
            img = self.crouch_imgs[int(self.img_count)]
            if abs(self.x_vel) < 0.55:
                if not self.looking_right:
                    img = pygame.transform.flip(img, True, False)
            self.img_count += 0.1
            offset_x, offset_y = (-35, -8)

        # Right Wall
        if self.on_rwall and not self.on_surface and self.slide_ability:
            self.img_count %= 2
            img = pygame.transform.flip(self.wall_slide_imgs[int(self.img_count)], True, False)
            self.img_count += 0.1
            offset_x = -35

        # Left Wall
        if self.on_lwall and not self.on_surface and self.slide_ability:
            self.img_count %= 2
            img = pygame.transform.flip(self.wall_slide_imgs[int(self.img_count)], False, False)
            self.img_count += 0.1
            offset_x = -35

        # Flipping based on speed
        if not abs(self.x_vel) < 0.55:
            if self.x_vel < 0 and not (self.on_rwall or self.on_lwall):
                img = pygame.transform.flip(img, True, False)
                self.looking_right = False
            elif self.x_vel > 0:
                self.looking_right = True

        surface.blit(img, (self.x + offset_x, self.y + offset_y))
        # pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, self.width, self.height), 2)
