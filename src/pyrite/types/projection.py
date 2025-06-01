from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygame import Rect


class Projection(ABC):

    @property
    @abstractmethod
    def far_plane(self) -> Rect:
        """
        A Rect describing the characteristics of the projection's far plane.
        """

    @property
    @abstractmethod
    def z_near(self) -> float:
        """
        Distance of the near plane from the projection source.
        """

    @property
    @abstractmethod
    def z_far(self) -> float:
        """
        Distance of the far plane from the projection source.
        """

    @property
    @abstractmethod
    def z_depth(self) -> float:
        """
        Total depth of the projected area.
        """
