from __future__ import annotations

from typing import TYPE_CHECKING

from pygame import Vector2

from ..types import transform

if TYPE_CHECKING:
    from pygame.typing import Point


class Transform:

    def __init__(
        self, position: Point = (0, 0), rotation: float = 0, scale: Point = (1, 1)
    ) -> None:
        self._position = Vector2(position)
        self._rotation = rotation
        self._scale = Vector2(scale)

    @property
    def position(self) -> Vector2:
        """
        Represents the local position of the transform
        """
        return self._position

    @position.setter
    def position(self, new_position: Point):
        self._position = Vector2(new_position)

    @property
    def rotation(self) -> float:
        """
        Represents the local rotation of the transform
        """
        return self._rotation

    @rotation.setter
    def rotation(self, angle: float):
        self._rotation = angle

    @property
    def scale(self) -> Vector2:
        """
        Represents the local scaling of the transform
        """
        return self._scale

    @scale.setter
    def scale(self, new_scale: Point):
        self._scale = Vector2(new_scale)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, transform.TransformProtocol):
            return False
        return (
            value.position == self._position
            and value.rotation == self._rotation
            and value.scale == self._scale
        )

    def copy(self) -> Transform:
        return Transform(self._position, self._rotation, self._scale)

    def local_to(self, other_transform: transform.TransformProtocol) -> Transform:
        """
        Returns a new transform with the current transform's values

        :param other_transform: A transform-like object whose context is being shifted
            into.
        :return: A new transform, representing the current transform in the local space
            of _other_transform_
        """
        new_scale = self._scale.elementwise() * other_transform.scale
        new_rotation = self._rotation + other_transform.rotation
        new_position = (self._position.elementwise() * new_scale).rotate(
            -self._rotation
        )
        return Transform(new_position, new_rotation, new_scale)
