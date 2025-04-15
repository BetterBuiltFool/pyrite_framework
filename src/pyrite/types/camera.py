from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING


import pygame
from pygame import Vector2

if TYPE_CHECKING:
    from pygame.typing import Point
    from ..enum import Layer
    from .renderable import Renderable


class CameraBase:
    """
    Defines the important attributes of a camera for the sake of drawing onto its
    surface.

    Can be constructed from the window.
    """

    def __init__(
        self,
        surface: pygame.Surface,
        layer_mask: tuple[Layer] = None,
    ) -> None:
        self.surface = surface
        if layer_mask is None:
            layer_mask = ()
        self.layer_mask = layer_mask

    def clear(self):
        """
        Overwrite the surface to allow new drawing on top.
        Default fill is solid black.
        """
        self.surface.fill((0, 0, 0, 0))

    def cull(self, items: Iterable[Renderable]) -> Iterable[Renderable]:
        """
        Removes any renderables that do not fall within view of the camera.

        :param items: Any iterable containing the renderable to be culled.
        :return: A generator containing only renderables in view of the camera's
        viewport.
        """
        return (item for item in items if self._in_view(item.get_rect()))

    def _in_view(self, rect: pygame.Rect) -> bool:
        return self.surface.get_rect().colliderect(rect)

    def to_local(self, point: Point) -> Vector2:
        """
        Converts a point in world space to local space (The camera'ssurface)

        :param point: A point, in world space
        :return: The local space equivalent of _point_
        """
        return Vector2(point)

    def to_world(self, point: Point) -> Vector2:
        """
        Converts a point in local space (The camera's surface) to world space.

        :param point: A point, in local space
        :return: The world space equivalent of _point_
        """

        return Vector2(point)

    def screen_to_world(self, point: Point, sector_index: int = 0) -> Vector2:

        return Vector2(point)

    def screen_to_world_clamped(
        self, point: Point, sector_index: int = 0
    ) -> Vector2 | None:

        return Vector2(point)
