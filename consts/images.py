import os, pygame

BACKGROUND_MENU = pygame.image.load(
    os.path.join('res', 'assets', 'backgrounds', 'background_menu.png')
)

BACKGROUND_LEVEL1 = pygame.image.load(
    os.path.join('res', 'assets', 'backgrounds', 'background_level1.png')
)

BACKGROUND_LEVEL2 = pygame.image.load(
    os.path.join('res', 'assets', 'backgrounds', 'background_level2.png')
)





GIRL = pygame.image.load(
    os.path.join('res', 'assets', 'girl', 'stay.png')
)

GIRL_WALK = [
    pygame.image.load(
        os.path.join('res', "assets", "girl", f"walk_{i}.png")
        )
    for i in range(1, 13)
]





HEALER = pygame.image.load(
    os.path.join('res', 'assets', 'game_elements', 'healer.png')
)

TRAP = pygame.image.load(
    os.path.join('res', 'assets', 'game_elements', 'trap.png')
)





BLOCK = pygame.image.load(
    os.path.join('res', 'assets', 'blocks', 'block.png')
)