from __future__ import annotations

from pygame.typing import Point
from pygame import Surface, Vector2


class Transform:

    def __init__(self, position: Point) -> None:
        self._position = Vector2(position)

    @property
    def position(self) -> Vector2:
        return self._position

    @position.setter
    def position(self, new_position: Point):
        self._position = Vector2(new_position)

    def update_image(self, image: Surface) -> Surface:
        return image
