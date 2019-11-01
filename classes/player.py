import pygame


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

    slide_imgs = [pygame.image.load('images/player/wall_slide_cycle/adventurer-wall-slide-00.png'),
                  pygame.image.load('images/player/wall_slide_cycle/adventurer-wall-slide-01.png')]
    for i, img in enumerate(slide_imgs):
        slide_imgs[i] = pygame.transform.scale(img, scale)

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

    def cap_speed(self):
        if abs(self.x_vel) > abs(self.max_vel):
            self.x_vel = self.max_vel if self.x_vel > 0 else -self.max_vel

    def calculate_move(self):
        self.y_vel += 1
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

    def calculate_walljump(self, relative_y_vel):
        if self.jumping and self.on_lwall and not self.on_surface:
            self.y_vel = -15 * 0.707 + relative_y_vel
            self.x_vel -= 15 * 0.707

        if self.jumping and self.on_rwall and not self.on_surface:
            self.y_vel = -15 * 0.707 + relative_y_vel
            self.x_vel += 15 * 0.707

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

    def collide_tile(self, tile):
        touching_left, touching_right = False, False
        temp_x_rect = pygame.Rect(self.x + self.x_vel - tile.x_vel, self.y, self.width, self.height)
        if temp_x_rect.colliderect(tile.get_rect()):
            if self.x_vel - tile.x_vel > 0:
                self.x = tile.x - self.width
                self.x_vel = tile.x_vel
                touching_left = True

            else:
                self.x = tile.x + tile.width
                self.x_vel = tile.x_vel
                touching_right = True

        on_surface = False
        temp_y_rect = pygame.Rect(self.x, self.y + self.y_vel - tile.y_vel, self.width, self.height)
        if temp_y_rect.colliderect(tile.get_rect()):
            if self.y_vel - tile.y_vel > 0:
                self.y = tile.y - self.height
                self.y_vel = tile.y_vel
                on_surface = True

            else:
                self.y = tile.y + tile.width
                self.y_vel = tile.y_vel

        return on_surface, touching_right, touching_left, float(tile.y_vel) if temp_x_rect.colliderect(tile.get_rect()) else None

    def draw(self, surface):
        img = self.surface
        offset_x = -35
        offset_y = -8

        # Falling
        if not self.on_surface:
            self.img_count %= 2
            img = self.air_imgs[int(self.img_count)]
            self.img_count += 0.1
            offset_x, offset_y = (-42, -14)

        # Idle Falling
        if not self.on_surface and round(self.x_vel) == 0:
            self.img_count %= 2
            img = self.air_imgs[int(self.img_count)]
            if not self.looking_right:
                img = pygame.transform.flip(img, True, False)
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

        # Right Wall
        if self.on_rwall and not self.on_surface:
            self.img_count %= 2
            img = pygame.transform.flip(self.slide_imgs[int(self.img_count)], True, False)
            self.img_count += 0.1
            offset_x = -35

        # Left Wall
        if self.on_lwall and not self.on_surface:
            self.img_count %= 2
            img = pygame.transform.flip(self.slide_imgs[int(self.img_count)], False, False)
            self.img_count += 0.1
            offset_x = -35

        # Flipping based on speed
        if round(self.x_vel) == 0:
            pass
        elif self.x_vel < 0 and not (self.on_rwall or self.on_lwall):
            img = pygame.transform.flip(img, True, False)
            self.looking_right = False
        elif self.x_vel > 0:
            self.looking_right = True

        surface.blit(img, (self.x + offset_x, self.y + offset_y))
        # pygame.draw.rect(surface, (255, 0, 0), (self.x, self.y, self.width, self.height), 2)
