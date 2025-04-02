from __future__ import annotations

from pygame.typing import Point
from pygame import Vector2


class Transform:

    def __init__(
        self, position: Point = (0, 0), rotation: float = 0, scale: Point = (1, 1)
    ) -> None:
        self._position = Vector2(position)
        self._rotation = rotation
        self._scale = Vector2(scale)

    @property
    def position(self) -> Vector2:
        return self._position

    @position.setter
    def position(self, new_position: Point):
        self._position = Vector2(new_position)

    @property
    def rotation(self) -> float:
        return self._rotation

    @rotation.setter
    def rotation(self, angle: float):
        self._rotation = angle

    @property
    def scale(self) -> Vector2:
        return self._scale

    @scale.setter
    def scale(self, new_scale: Point):
        self._scale = Vector2(new_scale)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Transform):
            # Only a Transform or subclass can be equal.
            # If it's not even a Transform, why bother comparing further?
            return False
        return (
            value._position == self._position
            and value._rotation == self._rotation
            and value._scale == self._scale
        )
