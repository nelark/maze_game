import pygame
from game_objects.characters.base_character import Character
from game_objects.base_game_object import GameObject

class Health_changer(GameObject):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        img: pygame.surface.Surface,
        health_effect: int
    ):
        super().__init__(img=img, width=width, height=height)
        self._x = x
        self._y = y
        self._health_effect = health_effect

        self._object = pygame.Rect(self._x, self._y, self._width, self._height)


    def activate(self, player: Character, sound: pygame.mixer.Sound):
        if self._exist:
            sound.set_volume(0.1)
            sound.play()

            self._exist = False
            player.change_health(self._health_effect)