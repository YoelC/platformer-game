import pygame.freetype
import sys
from classes.player import Player
from classes.tile import Tile
from classes.button import Button
from classes.camera import Camera
from config import map, WINDOW_WIDTH, WINDOW_HEIGHT
import time

FPS = 30

pygame.init()
pygame.freetype.init()
win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

player = Player((WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
tiles = []
buttons = []
for y, row in enumerate(map):
    for x, tile in enumerate(row):
        if tile == 1 or tile == 2 or int(tile) == 4:
            tiles.append(Tile((x, y), tile))
        if int(tile) == 3:
            buttons.append(Button((x, y), tile))

camera = Camera(player)
for tile in tiles:
    camera.add_object(tile)
for button in buttons:
    camera.add_object(button)
camera.set_black_bars(True)

space = False
holding_space = False

e_key = False
holding_e_key = False
while True:
    clock.tick(FPS)

    # Handling input
    keys = pygame.key.get_pressed()

    # Space input
    space = False
    if keys[pygame.K_SPACE] and not holding_space:
        space = True
        holding_space = True

    if not keys[pygame.K_SPACE]:
        holding_space = False

    # 'E' input
    e_key = False
    if keys[pygame.K_e] and not holding_e_key:
        e_key = True
        holding_e_key = True

    if not keys[pygame.K_e]:
        holding_e_key = False

    pygame.display.set_caption(f'fps: {clock.get_fps()}')
    if pygame.QUIT in [event.type for event in pygame.event.get()]:
        sys.exit(0)

    if keys[pygame.K_a]:
        player.left()
    if keys[pygame.K_d]:
        player.right()
    if keys[pygame.K_s]:
        player.down()

    if space:
        player.jump()

    # Calculating movement with input
    player.calculate_move()

    # Calculating collision
    crashes_floor = []
    touches_lwall = []
    touches_rwall = []
    for tile in tiles:
        result = tile.collide_player(player)
        crashes_floor.append(result[0])
        touches_rwall.append(result[1])
        touches_lwall.append(result[2])

    player.on_surface = any(crashes_floor)
    player.on_rwall = any(touches_rwall)
    player.on_lwall = any(touches_lwall)

    # Relative y velocity for wall jumps
    player.calculate_walljump(0)
    player.move()

    button_collisions = []

    # Camera movement
    camera.move(player)

    # Checking for button presses
    player.attached_text = ''
    for button in buttons:
        collide_button = button.collide_player(player)
        if collide_button and not button.pressed:
            player.attached_text = 'Use'
            if e_key:
                button.was_pressed()

    player.use = any(button_collisions)

    # Syncing tiles with buttons
    for tile in tiles:
        tile.move()
        for button in buttons:
            if button.pressed and round(button.tile - 3, 2) == round(tile.tile - 4, 2) and tile.activated:

                tile.activate()

            if button.pressed and button.tile == 3.03:
                button.was_unpressed()
                camera.set_pos((0, 4))

    # Drawing
    win.fill((64, 64, 64))
    player.draw(win)
    player.reset_variables()

    for tile in tiles:
        tile.draw(win)

    for button in buttons:
        button.draw(win)

    player.draw_text(win)

    camera.draw_black_bar(win)
    # Deadzone drawing
    # camera.draw(win)

    pygame.display.flip()
