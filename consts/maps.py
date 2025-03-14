import os
from res.file_manager import read_map
from consts import window


OPEN_MAP_1, WALLS_MAP1, HEALERS_MAP1, TRIPS_MAP1, EXITS_MAP1 = read_map(file_map=os.path.join('res', 'maps', 'level1.txt'),
    number_blocks=20,
    width_window=window.WIDTH,
    height_window=window.HEIGHT
    )


OPEN_MAP_2, WALLS_MAP2, HEALERS_MAP2, TRIPS_MAP2, EXITS_MAP2 = read_map(file_map=os.path.join('res', 'maps', 'level2.txt'),
    number_blocks=20,
    width_window=window.WIDTH,
    height_window=window.HEIGHT
    )