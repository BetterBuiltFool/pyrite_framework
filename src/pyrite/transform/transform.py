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
        transform in the same space as _root_.

        Inverse of Transform.localize()

        :param root: A transform-like object being treated like the new origin for the
            local transform.
        :return: A new transform, representing the current transform in the local space
            of _root_.
        """
        new_scale = self.scale.elementwise() * root.scale
        new_rotation = self.rotation + root.rotation

        scaled_position = self.position.elementwise() * root.scale
        rotated_position = scaled_position.rotate(-root.rotation)
        new_position = root.position + rotated_position

        return Transform(new_position, new_rotation, new_scale)

    def localize(self, root: transform.TransformProtocol) -> Transform:
        """
        Derives a local transform from _root_.

        Given both this transform and _root_ existing in the same space, finds the
        equivalent local transform from the difference between the two.

        Inverse of Transform.generalize()

        :param root: A transform-like object in the same space as the current transform.
        :return: A new transform, equivalent to the difference between the current
            transform and _root_.
        """

        translated_position = self.position - root.position
        rotated_position = translated_position.rotate(root.rotation)
        new_position = rotated_position.elementwise() / root.scale

        new_rotation = self.rotation - root.rotation

        new_scale = self.scale.elementwise() / root.scale

        return Transform(new_position, new_rotation, new_scale)
