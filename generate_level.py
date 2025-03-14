import pygame, os, sys
import consts.levels as lvl
from game_objects.characters.player import Player
from consts.window import *


def generate_menu_register(
    window: pygame.surface.Surface, username: str, player: Player
):
    import consts.fonts as font
    import consts.images as img
    import consts.sounds as sound
    import consts.maps as map
    from res.file_manager import write_data

    # Задаем переменные, которые будут хранить Surface текста
    text_ask_name = font.MENU.render("Введите ваше имя", True, "white")
    text_comment = font.MENU.render("Для подтверждения нажмите ENTER", True, "white")
    text_username = font.MENU.render(f"{username}", True, "white")

    # Накладываем фон и поверхности текстов
    window.blit(pygame.transform.scale(img.BACKGROUND_MENU, (WIDTH, HEIGHT)), (0, 0))
    window.blit(text_ask_name, (20, 30))
    window.blit(text_comment, (20, HEIGHT - 70))
    window.blit(text_username, (20, 90))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:

            """Если зажат Enter и username не пустой(пользователь успел уже что-то
            ввести в качестве ника), то выполняется регистрация"""
            if event.key == pygame.K_RETURN and username:
                write_data(
                    file=os.path.join("res", "user_data.txt"),
                    name_data="name",
                    value_data=username,
                )
                # устанавливаем координаты игрока для уровня 1
                player.set_coordinate(x=map.OPEN_MAP_1.x, y=map.OPEN_MAP_1.y)

                # записываем необходимые данные о пользователе
                write_data(
                    file=os.path.join("res", "user_data.txt"),
                    name_data="cur_level",
                    value_data="1",
                )

                write_data(
                    file=os.path.join("res", "user_data.txt"),
                    name_data="cur_hp",
                    value_data="100",
                )

                pygame.mixer.music.load(sound.BACKGROUND_LEVEL_PATH)
                pygame.mixer.music.set_volume(0.1)
                pygame.mixer.music.play(-1)

                return username, lvl.LEVEL_1

            elif event.key == pygame.K_BACKSPACE:
                username = username[:-1]

            else:
                 if (
                    event.unicode.lower() in "qwertyuiopasdfghjklzxcvbnmйцукенгшщзхъфывапролджэячсмитьбюё1234567890_"
                 ):
                     username += event.unicode

    """Возвращается значение username и осуществляется переход в новое состояние игры.
    Возврат username для того чтобы в дальнейшем в бессконечном цикле передаваться
    функции generate_menu_register в качестве нового значения username для корректной работы"""
    return username, lvl.REGISTER_MENU


def generate_login_menu(window: pygame.surface.Surface, username: str, player: Player):
    import consts.fonts as font
    import consts.images as img
    import consts.colors as color
    import consts.sounds as sound
    import consts.maps as map
    from res.file_manager import read_data

    text_welcome = font.MENU.render(f"Мы вас помним, {username}", True, color.WHITE)
    text_comment = font.MENU.render("Для начала игры нажмите ENTER", True, color.WHITE)

    window.blit(pygame.transform.scale(img.BACKGROUND_MENU, (WIDTH, HEIGHT)), (0, 0))
    window.blit(text_welcome, (20, 30))
    window.blit(text_comment, (20, HEIGHT - 70))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            """При нажатии на Enter вызывается информация об уровне, на котором остановился игрок.
            После происходит обработка данной информации и возврат необходимого состояния
            """
            if event.key == pygame.K_RETURN:
                # включаем музыку заднего фона для уровня
                pygame.mixer.music.load(sound.BACKGROUND_LEVEL_PATH)
                pygame.mixer.music.set_volume(0.1)
                pygame.mixer.music.play(-1)

                cur_level = read_data(os.path.join("res", "user_data.txt"), "cur_level")

                if cur_level == 1:
                    # устанавливаем координаты игрока для уровня 1
                    player.set_coordinate(x=map.OPEN_MAP_1.x, y=map.OPEN_MAP_1.y)

                    return lvl.LEVEL_1

                elif cur_level == 2:
                    # устанавливаем начальные координаты игрока для уровня 2
                    player.set_coordinate(x=map.OPEN_MAP_2.x, y=map.OPEN_MAP_2.y)

                    return lvl.LEVEL_2

    # Если пользователь не нажал на Enter или выход с игры, то возвращается текущее состояние
    return lvl.LOGIN_MENU


def generate_level_1(window: pygame.surface.Surface, player: Player):
    import consts.images as img
    import consts.maps as map
    import consts.sounds as sound
    from res.file_manager import read_data, write_data

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # устанавливаем сохраненное значение здоровья
    hp = read_data(
        file=os.path.join("res", "user_data.txt"),
        name_data="cur_hp",
    )
    player.set_health(hp)


    window.blit(pygame.transform.scale(img.BACKGROUND_LEVEL1, (WIDTH, HEIGHT)), (0, 0))
    
    # Осуществляем прорисовку стен для лабиринта
    image_block = pygame.transform.scale(img.BLOCK, (HEIGHT / 20, WIDTH / 20))
    for wall in map.WALLS_MAP1:
        window.blit(image_block, wall)

    # Прорисовка аптечек и проверка, пересекается ли пользователь с ними
    for healer in map.HEALERS_MAP1:
        healer.draw(window)
        if player.get_rect().colliderect(healer.get_rect()):
            healer.activate(player=player, sound=sound.HEAL)

    # Прорисовка ловушек и проверка, пересекается ли пользователь с ними
    for trap in map.TRIPS_MAP1:
        trap.draw(window)
        if player.get_rect().colliderect(trap.get_rect()):
            trap.activate(player=player, sound=sound.DAMAGE)
    
    # проверяем движение игрока
    player.walk(
        window_width=WIDTH, window_height=HEIGHT, collide_objects=[map.WALLS_MAP1]
    )

    # Прорисовываем игрока и его здоровье
    player.draw(window)
    player.draw_hp(window=window, coords=(WIDTH - 100, 0))

    """проверяем, пересекся ли игрок с точками выхода из уровня. Если пересекся - 
    переходим на новый уровень и переписываем данные игрока. Иначе - остаемся
    на текущем уровне"""
    for exit in map.EXITS_MAP1:
        if player.get_rect().colliderect(exit):
            sound.WIN.play()
            write_data(
                file=os.path.join("res", "user_data.txt"),
                name_data="cur_level",
                value_data="2",
            )

            # устанавливаем координаты игрока на новором уровне
            player.set_coordinate(x=map.OPEN_MAP_2.x, y=map.OPEN_MAP_2.y)

            return lvl.LEVEL_2
        return lvl.LEVEL_1


def generate_level_2(window: pygame.surface.Surface, player: Player):
    import consts.images as img
    import consts.maps as map
    import consts.sounds as sound
    from res.file_manager import read_data, write_data

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # устанавливаем сохраненное значение здоровья
    hp = read_data(
        file=os.path.join("res", "user_data.txt"),
        name_data="cur_hp",
    )
    player.set_health(hp)


    window.blit(pygame.transform.scale(img.BACKGROUND_LEVEL2, (WIDTH, HEIGHT)), (0, 0))
    
    # Осуществляем прорисовку стен для лабиринта
    image_block = pygame.transform.scale(img.BLOCK, (HEIGHT / 20, WIDTH / 20))
    for wall in map.WALLS_MAP2:
        window.blit(image_block, wall)

    # Прорисовка аптечек и проверка, пересекается ли пользователь с ними
    for healer in map.HEALERS_MAP2:
        healer.draw(window)
        if player.get_rect().colliderect(healer.get_rect()):
            healer.activate(player=player, sound=sound.HEAL)

    # Прорисовка ловушек и проверка, пересекается ли пользователь с ними
    for trap in map.TRIPS_MAP2:
        trap.draw(window)
        if player.get_rect().colliderect(trap.get_rect()):
            trap.activate(player=player, sound=sound.DAMAGE)
    
    # проверяем движение игрока
    player.walk(
        window_width=WIDTH, window_height=HEIGHT, collide_objects=[map.WALLS_MAP2]
    )

    # Прорисовываем игрока и его здоровье
    player.draw(window)
    player.draw_hp(window=window, coords=(WIDTH - 100, 0))


    for exit in map.EXITS_MAP2:
        if player.get_rect().colliderect(exit):
            sound.WIN.play()
            write_data(
                file=os.path.join("res", "user_data.txt"),
                name_data="cur_level",
                value_data="1",
            )
            write_data(
                file=os.path.join("res", "user_data.txt"),
                name_data="cur_hp",
                value_data="100",
            )

            # включаем музыку заднего фона для меню финиша
            pygame.mixer.music.load(sound.BACKGROUND_MENU_PATH)
            pygame.mixer.music.set_volume(0.1)
            pygame.mixer.music.play(-1)
            return lvl.FINISH
        return lvl.LEVEL_2
    

def generate_finish(window: pygame.surface.Surface):
    import consts.fonts as font
    import consts.images as img
    import consts.colors as color

    text_welcome = font.MENU.render(f"Поздравляем вас! Вы прошли игру", True, color.WHITE)
    text_comment = font.MENU.render("Нажмите Enter чтобы выйти", True, color.WHITE)

    window.blit(pygame.transform.scale(img.BACKGROUND_MENU, (WIDTH, HEIGHT)), (0, 0))
    window.blit(text_welcome, (20, 30))
    window.blit(text_comment, (20, HEIGHT-70))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                sys.exit()

    return lvl.FINISH


def death(player: Player):
    from res.file_manager import write_data
    import consts.images as img
    import consts.maps as map

    write_data(
                file=os.path.join("res", "user_data.txt"),
                name_data="cur_level",
                value_data="1",
        )
    write_data(
                file=os.path.join("res", "user_data.txt"),
                name_data="cur_hp",
                value_data="100",
        )

    player = Player(
    img=img.GIRL,
    width=WIDTH // 25,
    height=HEIGHT // 25,
    max_hp=100,
    vel=3,
    walk_animation=img.GIRL_WALK
        )
    
    player.set_coordinate(x=map.OPEN_MAP_1.x, y=map.OPEN_MAP_1.y)

    return lvl.LEVEL_1, player
