import pygame, os

import consts.levels as lvl
from generate_level import *

from consts.window import WIDTH, HEIGHT, FPS
import consts.images as img
import consts.sounds as sound

from res.file_manager import read_data

from game_objects.characters.player import Player


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = Player(
    img=img.GIRL,
    width=WIDTH // 25,
    height=HEIGHT // 25,
    max_hp=100,
    vel=3,
    walk_animation=img.GIRL_WALK
)


username = read_data(file=os.path.join("res", "user_data.txt"), name_data='name')
if username is None:
    username = str()
    game_station = lvl.REGISTER_MENU
else:
    game_station = lvl.LOGIN_MENU


# включаем музыку заднего фона для меню
pygame.mixer.music.load(sound.BACKGROUND_MENU_PATH)
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)
while True:
    if game_station == lvl.REGISTER_MENU:
        username, game_station = generate_menu_register(screen, username, player)
    elif game_station == lvl.LOGIN_MENU:
        game_station = generate_login_menu(screen, username, player)
    elif game_station == lvl.LEVEL_1:
        game_station = generate_level_1(screen, player)
    elif game_station == lvl.LEVEL_2:
        game_station = generate_level_2(screen, player)
    elif game_station == lvl.FINISH:
        game_station = generate_finish(screen)

    hp = player.get_hp()
    if hp <= 0:
        game_station, player = death(player)

    pygame.display.update()
    clock.tick(FPS)