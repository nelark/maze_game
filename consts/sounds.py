import pygame, os

pygame.init()

BACKGROUND_MENU_PATH = os.path.join('res', 'sounds', 'background', 'background_menu.mp3')
BACKGROUND_LEVEL_PATH = os.path.join('res', 'sounds', 'background', 'background_level.mp3')

WIN = pygame.mixer.Sound(os.path.join('res', 'sounds', 'game', 'win.ogg'))
DAMAGE = pygame.mixer.Sound(os.path.join('res', 'sounds', 'game', 'damage.ogg'))
HEAL = pygame.mixer.Sound(os.path.join('res', 'sounds', 'game', 'heal.ogg'))