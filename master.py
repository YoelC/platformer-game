import pygame.freetype
import sys
from classes.player import Player
from classes.tile import Tile
from classes.water import WaterTile
from classes.note_tile import NoteTile
from classes.button import Button
from classes.camera import Camera
from config import map, WINDOW_WIDTH, WINDOW_HEIGHT

FPS = 30

pygame.init()
pygame.freetype.init()
win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

player = Player((WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
tiles = []
buttons = []
water_tiles = []
note_tiles = []
for y, row in enumerate(map):
    for x, tile in enumerate(row):
        if tile == 1 or tile == 2 or int(tile) == 4:
            tiles.append(Tile((x, y), tile))
        if int(tile) == 3:
            buttons.append(Button((x, y), tile))
        if int(tile) == 5:
            note_tiles.append(NoteTile((x, y), tile))
        if tile == 8:
            water_tiles.append(WaterTile((x, y), tile))

camera = Camera(player)
for tile in tiles:
    camera.add_object(tile)
for button in buttons:
    camera.add_object(button)
for water_tile in water_tiles:
    camera.add_object(water_tile)
for note_tile in note_tiles:
    camera.add_object(note_tile)

camera.set_pos((0, -64*17))
player.center()

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
    if keys[pygame.K_w]:
        player.up()

    if space:
        player.jump()

    # Water tiles
    in_water = []
    for tile in water_tiles:
        in_water.append(player.get_rect().colliderect(tile.get_rect()))

    player.underwater = any(in_water)

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
    camera.note.move()

    if camera.y < -64*29:
        camera.set_pos((64 * 25, -64 * 5 + 16))
        player.center()

    if player.moving_down and player.on_surface:
        camera.set_black_bars(True)
    else:
        camera.set_black_bars(False)

    # Checking for button presses
    player.attached_text = ''
    for button in buttons:
        collide_button = button.collide_player(player)
        if collide_button and not button.pressed:
            player.attached_text = 'Use (E)'
            if e_key:
                button.was_pressed()

    player.use = any(button_collisions)

    # Syncing tiles with buttons
    for tile in tiles:
        tile.move()
        for button in buttons:
            if button.pressed and round(button.tile - 3, 2) == round(tile.tile - 4, 2) and tile.activated:
                tile.activate()

    # Note tile interaction
    readings = []
    for note_tile in note_tiles:
        read = note_tile.get_rect().colliderect(player.get_rect())
        readings.append(read)
        if read:
            player.use = True
            player.attached_text = 'Read (E)'
            if e_key:
                camera.note.set_text(note_tile.text)
                player.reading = True
                camera.note.set_pos(50)

    if not any(readings):
        camera.note.set_pos(WINDOW_HEIGHT + 100)
        player.reading = False

    if player.reading:
        camera.set_black_bars(True)

    # Drawing
    win.fill((64, 64, 64))
    player.draw(win)
    player.reset_variables()

    for tile in tiles:
        tile.draw(win)

    for button in buttons:
        button.draw(win)

    player.draw_text(win)

    for water_tile in water_tiles:
        water_tile.draw(win)

    for note_tile in note_tiles:
        note_tile.draw(win)

    camera.draw_black_bar(win)
    camera.note.draw(win)
    # Deadzone drawing
    # camera.draw(win)

    pygame.display.flip()
