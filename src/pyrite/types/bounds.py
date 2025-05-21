from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygame import Rect
    from ..cuboid import Cuboid


class CullingBounds(ABC):

    @abstractmethod
    def get_volume(self) -> Cuboid:
        """
        Generates a volume representing the location of the bounds in 3D space.

        :return: A Cuboid that describes the bounds in 3D space.
            2D objects are represented by depth = 0.
        """
        pass

    @abstractmethod
    def flatten(self) -> Rect:
        """
        Generates an area representing the bounds in 2D space.

        :return: A Rect that describes the bounds in 2D space. 3D objects are projected
            onto a plane before the rect in calculated.
        """
        pass
