from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import TYPE_CHECKING


import pygame
from pygame import Vector2

if TYPE_CHECKING:
    from pygame import Surface
    from pygame.typing import Point
    from .renderable import Renderable


class CameraBase(ABC):
    """
    Defines the important attributes of a camera for the sake of drawing onto its
    surface.

    Can be constructed from the window.
    """

    @abstractmethod
    def clear(self):
        """
        Overwrite the surface to allow new drawing on top.
        Default fill is solid black.
        """
        pass

    def cull(self, items: Iterable[Renderable]) -> Iterable[Renderable]:
        """
        Removes any renderables that do not fall within view of the camera.

        :param items: Any iterable containing the renderable to be culled.
        :return: A generator containing only renderables in view of the camera's
        viewport.
        """
        pass

    @abstractmethod
    def draw_to_view(self, surface: Surface, position: Point):
        """
        Draws a surface to the camera's surface. Automatically converts the position
        into local space.

        :param surface: The source surface being drawn from.
        :param position: A point in world space where the surface is located.
        """
        pass

    def _in_view(self, rect: pygame.Rect) -> bool:
        pass
        # return self.surface.get_rect().colliderect(rect)

    @abstractmethod
    def to_local(self, point: Point) -> Vector2:
        """
        Converts a point in world space to local space (The camera'ssurface)

        :param point: A point, in world space
        :return: The local space equivalent of _point_
        """
        pass

    @abstractmethod
    def to_world(self, point: Point) -> Vector2:
        """
        Converts a point in local space (The camera's surface) to world space.

        :param point: A point, in local space
        :return: The world space equivalent of _point_
        """
        pass

    @abstractmethod
    def screen_to_world(self, point: Point, sector_index: int = 0) -> Vector2:
        pass

    @abstractmethod
    def screen_to_world_clamped(
        self, point: Point, sector_index: int = 0
    ) -> Vector2 | None:
        pass
