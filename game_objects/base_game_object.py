import pygame


class GameObject:
    def __init__(self, img: pygame.Surface, width: int, height: int) -> None:
        self._exist = True

        self._img = img
        self._width = width
        self._height = height

        self._object = pygame.Rect(0, 0, self._width, self._height)

    def draw(self, window: pygame.Surface) -> None:
        if self._exist:
            player_image = pygame.transform.scale(
                self._img, (self._object.width, self._object.height)
            )
            window.blit(player_image, self._object)

    def set_coords(self, x: int, y: int) -> None:
        self._object.x, self._object.y = x, y

    def set_size(self, width: int, height: int) -> None:
        self._width, self._height = width, height
        self._object.width, self._object.height = self._width, self._height

    def set_coordinate(self, x: int, y: int) -> None:
        self._object.x = x
        self._object.y = y

    def set_size(self, width: int, height: int) -> None:
        self._width = width
        self._height = height

    def get_rect(self) -> pygame.Rect:
        return self._object
