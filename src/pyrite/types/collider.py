from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygame import Rect, Vector2
    from ..transform import Transform


class Collider(ABC):

    @abstractmethod
    def get_aabb(self, transform: Transform) -> Rect:
        """
        Returns an axis-aligned bounding box for the collider.

        :transform: A Transform object representing the center of the collider in world
            space.
        """
        pass

    @abstractmethod
    def collide(
        self,
        collide_with: Collider,
        delta_transform: Transform,
    ) -> bool:
        """
        Does detailed collision detection against the other collider.

        :param collide_with: Another collider to be compared against.
        :param delta_transform: A Transform representing the difference in transform
            values between the two colliders' centers.
        :return: True if the colliders intersect, False otherwise.
        """
        pass

    @abstractmethod
    def _gjk_support_function(self, vector: Vector2, transform: Transform) -> Vector2:
        """
        Gets the furthest point of the shape in the direction provided by the vector

        :param vector: A normalized vector indicating a direction
        :param transform: A transform indicating the world-space center of the collider.
        :return: A position, in world space, representing the furthest point in that
            direction.
        """
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
