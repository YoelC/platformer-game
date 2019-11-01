import pygame
import sys
from classes.player import Player
from classes.tile import Tile

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 768
WINDOW_WIDTH_TILES = int(WINDOW_WIDTH / 64)
WINDOW_HEIGHT_TILES = int(WINDOW_HEIGHT / 64)
FPS = 30

pygame.init()
win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

player = Player((WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

# This is the map. Each 0 is represented as an empty space, and 1 as a tile. 2 is the player spawn point.
map = [
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 2, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       ]

tiles = []
for y, row in enumerate(map):
    for x, tile in enumerate(row):
        if tile == 1:
            tiles.append(Tile((x, y)))

space = False
holding_space = False
while True:
    clock.tick(FPS)

    # Handling input
    keys = pygame.key.get_pressed()

    space = False
    if keys[pygame.K_SPACE] and not holding_space:
        space = True
        holding_space = True

    if not keys[pygame.K_SPACE]:
        holding_space = False

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
    relative_y_vels = []
    for tile in tiles:
        result = player.collide_tile(tile)
        crashes_floor.append(result[0])
        touches_rwall.append(result[1])
        touches_lwall.append(result[2])
        relative_y_vels.append(result[3])

    player.on_surface = any(crashes_floor)
    player.on_rwall = any(touches_rwall)
    player.on_lwall = any(touches_lwall)

    # Relative y velocity for wall jumps
    relative_y_vel = [relative_y_vel for relative_y_vel in relative_y_vels if isinstance(relative_y_vel, float)]
    if not relative_y_vel:
        relative_y_vel = 0
    else:
        relative_y_vel = relative_y_vel[0]

    player.calculate_walljump(0)
    player.move()
    for tile in tiles:
        tile.move()

    # Adjusting scroll
    x_scroll = 0
    y_scroll = 0
    player.x -= x_scroll
    player.y -= y_scroll
    for tile in tiles:
        tile.x -= x_scroll
        tile.y -= y_scroll

    win.fill((0, 0, 0))
    player.draw(win)
    player.reset_variables()

    for tile in tiles:
        tile.draw(win)

    pygame.display.flip()
