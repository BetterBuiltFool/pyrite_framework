from __future__ import annotations

from typing import TYPE_CHECKING


import pygame
from pygame import Vector2

from ..rendering.view_plane import ViewPlane

from ..types import CameraBase

if TYPE_CHECKING:
    from pygame import Surface
    from pygame.typing import Point
    from ..enum import Layer
    from ..types import Renderable


class DefaultCamera(CameraBase):
    """
    Defines the important attributes of a camera for the sake of drawing onto its
    surface.

    Can be constructed from the window.
    """

    def __init__(
        self,
        surface: Surface,
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

    def cull(self, renderable: Renderable) -> bool:
        """
        Compares the bounds of the renderable to the camera's view bounds to determine
        if the renderable should be rendered.

        :param renderable: Any renderable item to be drawn.
        :return: True if the renderable is visible and should be drawn, otherwise False.
        """
        bounds = renderable.get_bounds()
        return self.get_view_bounds().contains(bounds)

    # def cull(self, items: Iterable[Renderable]) -> Iterable[Renderable]:
    #     """
    #     Removes any renderables that do not fall within view of the camera.

    #     :param items: Any iterable containing the renderable to be culled.
    #     :return: A generator containing only renderables in view of the camera's
    #     viewport.
    #     """
    #     return (item for item in items if self._in_view(item.get_rect()))

    def draw_to_view(self, surface: Surface, position: Point):
        """
        Draws a surface to the camera's surface. Automatically converts the position
        into local space.

        :param surface: The source surface being drawn from.
        :param position: A point in world space where the surface is located.
        """
        self.surface.blit(surface, self.to_local(position))

    def get_view_bounds(self) -> ViewPlane:
        # TODO Find a way of caching this per frame so we don't regenerate it for each
        # renderable.
        return ViewPlane(self.surface.get_rect())

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
