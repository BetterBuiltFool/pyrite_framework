from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygame import Rect
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
