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

    def generalize(self, root: transform.TransformProtocol) -> Transform:
        """
        Applies one transform onto another, generalizing it into the same space as the
        first.

        This treats the transform as local to _root_, and finds the equivalent
        transform in the same sapce as _root_.

        :param root: A transform-like object whose context is being shifted
            into.
        :return: A new transform, representing the current transform in the local space
            of _root_
        """
        new_scale = self._scale.elementwise() * root.scale
        new_rotation = self._rotation + root.rotation

        scaled_position = self._position.elementwise() * new_scale
        rotated_position = scaled_position.rotate(-root.rotation)
        new_position = root.position + rotated_position

        return Transform(new_position, new_rotation, new_scale)
