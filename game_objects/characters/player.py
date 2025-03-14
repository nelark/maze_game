import pygame
from game_objects.characters.base_character import Character


class Player(Character):
    def draw_hp(self, window: pygame.surface.Surface, coords: tuple[int]) -> None:
        import consts.colors as color
        import consts.fonts as font

        text_hp = font.HP.render(f"HP: {self._cur_hp}", True, color.HP)
        window.blit(text_hp, coords)
