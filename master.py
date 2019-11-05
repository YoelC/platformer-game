import pygame.freetype
from config import map, WINDOW_WIDTH, WINDOW_HEIGHT
pygame.init()
pygame.freetype.init()
win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

from classes.player import Player
from classes.tile import Tile
from classes.water import WaterTile
from classes.note_tile import NoteTile
from classes.button import Button
from classes.door import Door
from classes.camera import Camera
from classes.particle import Particle
from classes.background import Background
from random import randint, uniform
import sys

FPS = 30

player = Player((WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
tiles = []
buttons = []
water_tiles = []
note_tiles = []
background = Background()
door_tiles = []
platform_tiles = []
for y, row in enumerate(map):
    for x, tile in enumerate(row):
        if tile == 1 or tile == 2 or int(tile) == 4:
            tiles.append(Tile((x, y), tile))
        if round(tile, 2) == 1.50:
            platform_tiles.append(Tile((x, y), tile, height=4))
        if int(tile) == 3:
            buttons.append(Button((x, y), tile))
        if int(tile) == 5:
            note_tiles.append(NoteTile((x, y), tile))
        if int(tile) == 6 or int(tile) == 7:
            door_tiles.append(Door((x, y), tile))
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
for door_tile in door_tiles:
    camera.add_object(door_tile)
for platform_tile in platform_tiles:
    camera.add_object(platform_tile)
camera.add_object(background)

space = False
holding_space = False
black_fadeout = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
black_fadeout.fill((0, 0, 0, 0))
alpha = 0

particles = []

e_key = False
holding_e_key = False

tick = 0
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

    # Door tiles
    was_here = False
    player.use = False
    door_collisions = []
    for door_tile in door_tiles:
        collide = door_tile.get_rect().colliderect(player.get_rect())
        door_collisions.append(collide)
        if collide:
            player.use = True
            player.attached_text = 'Enter (E)'
            if e_key:
                to_go = round(door_tile.tile - 1, 2)
                if int(door_tile.tile) == 6:
                    to_go = round(door_tile.tile + 1, 2)
                if not was_here:
                    was_here = True
                    camera.go_to(to_go)
                    alpha = 255

    # Calculating movement with input
    player.calculate_move()

    # Calculating platform collision
    crashes_floor = []
    for platform_tile in platform_tiles:
        if player.y_vel > 0 and not player.moving_down and round(player.y + player.height, 2) <= round(platform_tile.y, 2):
            result = platform_tile.collide_player(player)
            crashes_floor.append(result[0])

    # Calculating collision
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

    # Player movement
    player.calculate_walljump(0)
    player.move()

    button_collisions = []

    # Camera movement
    camera.move(player)
    camera.note.move()

    if player.moving_down and player.on_surface:
        camera.set_black_bars(True)
    else:
        camera.set_black_bars(False)

    # Particle creation
    if abs(player.x_vel) > 10 and player.on_surface and tick % 3 == 0:
        particles.append(Particle(
            pos=(player.x + player.width/2, player.y + player.height, randint(4, 8)),
            vel=(-player.x_vel/8, randint(-10, -5)),
            color=(128, 128, 128),
            lifetime=15,
            gravity=True))
        camera.add_object(particles[-1])

    if (player.on_lwall or player.on_rwall) and not player.moving_down and tick % 8 == 0:
        particles.append(Particle(
            pos=(player.x + player.width / 2 + randint(-5, 5), player.y + player.height/2, randint(4, 8)),
            vel=(0, player.y_vel),
            color=(128, 128, 128),
            lifetime=15,
            gravity=True))
        camera.add_object(particles[-1])

    if (player.on_lwall or player.on_rwall) and player.jumping:
        for i in range(3):
            particles.append(Particle(
                pos=(player.x + player.width / 2 + randint(-5, 5), player.y + player.height/2, randint(4, 8)),
                vel=(player.x_vel * uniform(0.5, 0.9), randint(-10, -5)),
                color=(128, 128, 128),
                lifetime=15,
                gravity=True))
            camera.add_object(particles[-1])

    # Checking for button presses
    for button in buttons:
        collide_button = button.collide_player(player)
        if collide_button and not button.pressed:
            player.attached_text = 'Use (E)'
            player.use = True
            if e_key:
                button.was_pressed()

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

    # Moving particles
    for i, particle in enumerate(particles):
        particles[i].move()
        if particle.dead:
            particles.pop(i)

    # Drawing
    win.fill((6, 9, 14))

    # Background drawing
    background.draw(win)

    '''
    for door_tile in door_tiles:
        door_tile.draw(win)
    '''

    for particle in particles:
        particle.draw(win)

    '''
    for platform_tile in platform_tiles:
        platform_tile.draw(win)
    '''

    player.draw(win)
    player.reset_variables()

    '''
    for tile in tiles:
        tile.draw(win)
    '''

    for button in buttons:
        button.draw(win)

    if player.use:
        player.draw_text(win)

    for water_tile in water_tiles:
        water_tile.draw(win)

    '''
    for note_tile in note_tiles:
        note_tile.draw(win)
    '''

    camera.draw_black_bar(win)
    camera.note.draw(win)

    # Deadzone drawing
    # camera.draw(win)

    alpha /= 1.1
    black_fadeout.fill((0, 0, 0, alpha))
    win.blit(black_fadeout, (0, 0))

    tick += 1

    pygame.display.flip()
