from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygame import Rect, Vector3
    from pygame.typing import Point


class Projection(ABC):

    @property
    @abstractmethod
    def far_plane(self) -> Rect:
        """
        A Rect describing the characteristics of the projection's far plane.
        """

    @abstractmethod
    def screen_to_NDC(self, screen_point: Point, viewport: Rect) -> Vector3:
        """
        Takes a point on the screen and converts it into NDC space.
        The NDC point is along the back plane of NDC space, for allowing ray casting.

        :param screen_point: A point in screen space.
        :param viewport: A Rect describing the viewport the screen point is in.
        :return: A 3D point in standard NDC space.
        """
        pass
