from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from pygame import Vector2

if TYPE_CHECKING:
    from pygame import Surface
    from pygame.typing import Point
    from .renderable import Renderable
    from ..enum import Layer
    from ..types.view_bounds import CameraViewBounds


class CameraBase(ABC):
    """
    Defines the important attributes of a camera for the sake of drawing onto its
    surface.

    Can be constructed from the window.
    """

    layer_mask: tuple[Layer]

    @abstractmethod
    def clear(self):
        """
        Overwrite the surface to allow new drawing on top.
        Default fill is solid black.
        """
        pass

    @abstractmethod
    def cull(self, renderable: Renderable) -> bool:
        """
        Compares the bounds of the renderable to the camera's view bounds to determine
        if the renderable should be rendered.

        :param renderable: Any renderable item to be drawn.
        :return: True if the renderable is visible and should be drawn, otherwise False.
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

    @abstractmethod
    def get_view_bounds(self) -> CameraViewBounds:
        """
        Gets the bounds object that represents the visible space of the camera.

        :return: A CameraViewBounds object describing the viewed space.
        """

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
