from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygame import FRect, Rect
    from pygame.typing import Point


class Projection(ABC):

    @property
    @abstractmethod
    def far_plane(self) -> Rect:
        """
        A Rect describing the characteristics of the projection's far plane.
        """

    @abstractmethod
    def screen_to_NDC(self, screen_point: Point, viewport: FRect) -> Point:
        pass
