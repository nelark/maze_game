import pygame


def read_data(file: str, name_data: str):
    with open(file, "r") as user_data:
        # преобразуем текст файла в список, в котором  каждый элемент - новая строка
        data = user_data.read().split("\n")

        for i in range(len(data)):
            # делим каждый элемент текущего на новый список вида [ключ: значение]
            new_el = data[i].split(":")

            # преобразование строчных типов в NoneType и Integer в случае необходимости
            if new_el[1] == "None":
                new_el[1] = None

            elif new_el[1].isdigit():
                new_el[1] = int(new_el[1])

            data[i] = new_el
        # преобразуем получившийся список в словарь
        data = dict(data)

        output_data = data[name_data]
        return output_data


def write_data(file: str, name_data: str, value_data: str):
    with open(file, "r") as user_data:
        # преобразуем текст файла в список, в котором  каждый элемент - новая строка
        data = user_data.read().split("\n")

        # изменяем содержимое необходимой нам строки
        for i in range(len(data)):
            if name_data in data[i]:
                data[i] = f"{name_data}:{value_data}"
        # преобразуем результат к строке
        data = "\n".join(data)

    with open(file, "w") as user_data:
        # производим перезапись файла
        user_data.write(f"{data}")


def read_map(file_map: str, number_blocks: int, width_window: int, height_window: int):
    from game_objects.game_changers.health_changer import Health_changer
    from consts.images import HEALER, TRAP
    
    open_level_object = None
    walls = []
    heal_objects = []
    debuff_objects = []
    close_level_objects = []

    with open(file_map, "r") as map:
        row, col = 0, 0

        # вычисляем ширину для блока в пикселях
        col_size = width_window // number_blocks
        row_size = height_window // number_blocks

        for line in map.read().split("\n"):
            line = line.split(" ")
            col = 0

            # 0 - пустота
            # 1 - начало уровня
            # 2 - блоки
            # 3 - аптечки
            # 4 - ловушки
            # 5 - выход из уровня
            for el in line:
                if el == "1":
                    open_level_object = pygame.Rect(col * col_size, row * row_size, col_size, row_size)
                elif el == "2":
                    walls.append(pygame.Rect(col * col_size, row * row_size, col_size, row_size))
                elif el == "3":
                    heal_objects.append(
                        Health_changer(
                            x=col * col_size,
                            y=row * row_size,
                            height=col_size,
                            width=row_size,
                            img=HEALER,
                            health_effect=10,
                        )
                    )
                elif el == "4":
                    debuff_objects.append(
                        Health_changer(
                            x=col * col_size,
                            y=row * row_size,
                            height=col_size,
                            width=row_size,
                            img=TRAP,
                            health_effect=-10,
                        )
                    )
                elif el == "5":
                    close_level_objects.append(pygame.Rect(col * col_size, row * row_size, col_size, row_size))

                col += 1

            row += 1

    return open_level_object, walls, heal_objects, debuff_objects, close_level_objects