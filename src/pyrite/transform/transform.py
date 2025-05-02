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
        Applies a root transform to a local transform, converting it into the same
        relative space.

        Can also be done with the * operator.

        Can be stacked with other generalizations and localizations to convert from any
        reference frame to another.

        Inverse of Transform.localize()

        :Example:
        ```
        local_transform = Transform((5, 0), 0, (1, 1))
        root_transform = Transform((10, 10), 90, (2, 2))

        local_transform.generalize(root_transform) == Transform((10, 0), 90, (2, 2))
        ```

        _______________________________________________________________________________

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

    def generalize_position(self, position: Vector2) -> Vector2:
        """
        Takes a position local to the Transform and converts it into the same relative
        space as the Transform.

        :Example:
        ```
        transform = Transform((10, 10), 0, (2,2))
        position = Vector2(5,5)

        transform.generalize_position(position) == Vector2(20, 20)
        ```
        _______________________________________________________________________________

        :param position: A position (as a Vector2) that is local to this Transform.
        :return: A new Vector2 position in the same relative space as this Transform.
        """
        scaled_position = self.scale.elementwise() * position
        rotated_position = scaled_position.rotate(-self.rotation)
        return self.position + rotated_position

    def __mul__(self, other_transform: transform.TransformProtocol) -> Transform:
        return Transform.generalize(other_transform, self)

    def __rmul__(self, other_transform: transform.TransformProtocol) -> Transform:
        return Transform.generalize(self, other_transform)

    def localize(self, root: transform.TransformProtocol) -> Transform:
        """
        Given two Transforms in the same relative space, finds the Transform local to
        the root that is equivalent of this Transform.

        Inverse of Transform.generalize()

        Can be stacked with other localizations and generalizations to convert from any
        reference frame to another.

        :Example:
        ```
        branch_transform = Transform((10, 0), 90, (2, 2))
        root_transform = Transform((10, 10), 90, (2, 2))

        branch_transform.localize(root_transform) == Transform((5, 0), 0, (1, 1))
        ```

        _______________________________________________________________________________

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

    def localize_position(self, position: Vector2) -> Vector2:
        """
        Takes a position in the same relative space as the Transform, and derives it in
        the local space of the Transform.

        :Example:
        transform = Transform((10, 10), 0, (2,2))
        position = Vector2(20, 20)

        transform.generalize_position(position) == Vector2(5, 5)

        :param position: A position (as a Vector2) that is local to this Transform.
        :return: A new Vector2 position in the same relative space as this Transform.
        """
        translated_position = position - self.position
        rotated_position = translated_position.rotate(self.rotation)
        return rotated_position / self.scale.elementwise()
