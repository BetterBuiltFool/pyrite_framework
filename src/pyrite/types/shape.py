from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from pygame import Rect

if TYPE_CHECKING:
    from pygame import Vector2
    from ..transform import Transform

DIRECTIONS: dict[str, Vector2] = {
    "up": Vector2(0, 1),
    "right": Vector2(1, 0),
    "down": Vector2(0, -1),
    "left": Vector2(-1, 0),
}


class Shape(ABC):

    def get_aabb(self, transform: Transform) -> Rect:
        """
        Returns an axis-aligned bounding box for the collider.

        :transform: A Transform object representing the center of the collider in world
            space.
        """
        extents = self._get_extents(transform)
        top = extents["up"].y
        left = extents["left"].x
        height = top - extents["down"].y
        width = extents["right"].x - left
        return Rect(left_top=(left, top), width_height=(width, height))

    @abstractmethod
    def get_furthest_vertex(self, vector: Vector2, transform: Transform) -> Vector2:
        """
        Gets the furthest point of the shape in the direction provided by the vector

        :param vector: A normalized vector indicating a direction
        :param transform: A transform indicating the world-space center of the collider.
        :return: A position, in world space, representing the furthest point in that
            direction.
        """
        pass

    @abstractmethod
    def _get_extents(self, transform: Transform) -> dict[str, Vector2]:
        pass

    def _prescale_vector(self, vector: Vector2, transform: Transform) -> Vector2:
        """
        Performs a standard translation of a vector into local space of the transform.

        :param vector: A direction vector
        :param transform: A transform representing localization data for the vector
        :return: The corrected vector, normalized
        """
        vector = vector.elementwise() / transform.scale
        vector = vector.rotate(-transform.rotation)
        return vector.normalize()
