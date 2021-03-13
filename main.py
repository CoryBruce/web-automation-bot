import pygame, sys

#https://www.youtube.com/watch?v=l-GUfEJcTH4

clock = pygame.time.Clock()
from pygame.locals import *
pygame.init()

pygame.display.set_caption("2d Action RPG")
WINDOW_SIZE = (600, 400)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)
display = pygame.Surface((300, 200))

deep_image = pygame.image.load('deep.png')
player_image = pygame.image.load('player_stand.png')
grass_image = pygame.image.load('grass.png')
dirt_image = pygame.image.load('dirt.png')
tall_grass_image = pygame.image.load('tall_grass.png')
is_left, is_right = False, False
player_y_momentum = 0
air_timer = 0
jump_speed = 3
player_speed = 4

true_scroll = [0, 0]

player_rect = Rect(50, 50, player_image.get_width(), player_image.get_height())
background_objects = [[0.25, [120, 10, 70, 400]], [0.25, [280, 30, 40, 400]], [0.5, [30, 40, 40, 400]], [0.5, [130, 90, 100, 400]], [0.5, [300, 80, 120, 400]]]

tilesize = 16

def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'left': False, 'right': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        if movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

game_map = load_map('map')

RED = [255, 0, 0]
WHITE = [255, 255, 255, 255]
BLACK = [0, 0, 0]


system_on = True
while system_on:
    display.fill(BLACK)

    true_scroll[0] += (player_rect.x - true_scroll[0] - (display.get_width()/2 + 2))/20
    true_scroll[1] += (player_rect.y - true_scroll[1] - (display.get_height()/2 + 6))/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    pygame.draw.rect(display, (7, 80, 75), pygame.Rect(0, 120, 300, 80))
    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0] - scroll[0] * background_object[0], background_object[1][1] - scroll[1] * background_object[0], background_object[1][2], background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(display, (14, 222, 150), obj_rect)
        else:
            pygame.draw.rect(display, (9, 91, 85), obj_rect)


    # draws map
    tile_rects = []
    y = 0
    for row in game_map:
        x = 0
        for tile in row:
            if tile == "1":
                display.blit(dirt_image, (x * tilesize - scroll[0], y * tilesize - scroll[1]))
            if tile == "2":
                display.blit(grass_image, (x * tilesize - scroll[0], y * tilesize - scroll[1]))
            if tile == '3':
                display.blit(deep_image, (x * tilesize - scroll[0], y * tilesize - scroll[1]))
            if tile == 'G':
                display.blit(tall_grass_image, (x * tilesize - scroll[0], y * tilesize - scroll[1]))
            if tile != "0":
                tile_rects.append(pygame.Rect(x * tilesize, y * tilesize, tilesize, tilesize))
            x += 1
        y += 1



    player_movement = [0, 0]
    if is_right:
        player_movement[0] += player_speed
    if is_left:
        player_movement[0] -= player_speed
    player_movement[1] += player_y_momentum
    player_y_momentum += 0.1
    if player_y_momentum > 3:
        player_y_momentum = 3

    player_rect, collisions = move(player_rect, player_movement, tile_rects)
    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
    else:
        air_timer += 1

    display.blit(player_image, (player_rect.x - scroll[0], player_rect.y - scroll[1]))

    # events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_a:
                is_left = True
            if event.key == K_d:
                is_right = True
            if event.key ==K_w:
                if air_timer < 6:
                    player_y_momentum = -jump_speed
        if event.type == KEYUP:
            if event.key == K_a:
                is_left = False
            if event.key ==K_d:
                is_right = False

    surface = pygame.transform.scale(display, WINDOW_SIZE) #draw everything to display surface then scale it up here
    screen.blit(surface, (0, 0))
    pygame.display.update()
    clock.tick(60)