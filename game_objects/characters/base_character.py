import pygame
import os
from res.file_manager import write_data
from game_objects.base_game_object import GameObject


class Character(GameObject):
    def __init__(
        self,
        img: pygame.Surface,
        width: int,
        height: int,
        max_hp: int,
        vel: int,
        walk_animation: list = None,
    ) -> None:

        super().__init__(img, width, height)
        self._cur_img = img

        self._max_hp = max_hp
        self._cur_hp = self._max_hp
        self._vel = vel
        self._walk_animation = walk_animation

        if self._walk_animation is not None:
            self._length_walk_animation = len(self._walk_animation)
            self._cur_walk_frame = 0


    # переопределение метода из род.класса
    def draw(self, window: pygame.Surface) -> None:
        if self._exist:
            player_image = pygame.transform.scale(
                self._cur_img, (self._object.width, self._object.height)
            )
            window.blit(player_image, self._object)


    def walk(
        self,
        window_width: int,
        window_height: int,
        collide_objects: list[list] = None,
        walk_sound: pygame.mixer.Sound = None,
    ) -> None:
        if self._exist:
            keys = pygame.key.get_pressed()
            original_position = self._object.topleft

            movement = True
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self._object.left > 0:
                self._object.x -= self._vel

            elif (
                keys[pygame.K_RIGHT] or keys[pygame.K_d]
            ) and self._object.right < window_width:
                self._object.x += self._vel

            elif (keys[pygame.K_UP] or keys[pygame.K_w]) and self._object.top > 0:
                self._object.y -= self._vel

            elif (
                keys[pygame.K_DOWN] or keys[pygame.K_s]
            ) and self._object.bottom < window_height:
                self._object.y += self._vel

            else:
                movement = False

            if movement:
                if collide_objects is not None:
                    for collide_list in collide_objects:
                        for object in collide_list:
                            if self._object.colliderect(object):
                                self._object.topleft = original_position

                if self._walk_animation is not None:
                    self._cur_img = self._walk_animation[self._cur_walk_frame]
                    self._cur_walk_frame += 1

                    if self._cur_walk_frame >= self._length_walk_animation:
                        self._cur_walk_frame = 0

                if walk_sound is not None:
                    walk_sound.set_volume(0.1)
                    walk_sound.play()

            else:
                self._cur_img = self._img


    def set_health(self, new_health: int) -> None:
        if new_health <= 0:
            self._exist = False

        elif new_health <= self._max_hp:
            self._cur_hp = new_health
            write_data(
                file=os.path.join("res", "user_data.txt"),
                name_data="cur_hp",
                value_data=f"{self._cur_hp}",
            )

    def change_health(self, changing_health: int) -> None:
        new_health = self._cur_hp + changing_health

        if new_health <= 0:
            self._cur_hp = 0
            self._exist = False

        elif new_health <= self._max_hp:
            self._cur_hp += changing_health
            write_data(
                file=os.path.join("res", "user_data.txt"),
                name_data="cur_hp",
                value_data=f"{self._cur_hp}",
            )

    
    def get_hp(self) -> int:
        return self._cur_hp
