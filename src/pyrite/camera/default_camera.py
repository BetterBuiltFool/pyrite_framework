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

    # TODO Break out the window camera specific code into its own class so Camera
    # doesn't have a surface attribute.

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
        self.surface.fill((0, 0, 0, 0))

    def cull(self, renderable: Renderable) -> bool:
        bounds = renderable.get_bounds()
        return self.get_view_bounds().contains(bounds)

    def draw_to_view(self, surface: Surface, position: Point):
        # TODO Remove this
        self.surface.blit(surface, self.to_local(position))

    def get_view_bounds(self) -> ViewPlane:
        # TODO Find a way of caching this per frame so we don't regenerate it for each
        # renderable.
        return ViewPlane(self.surface.get_rect())

    def _in_view(self, rect: pygame.Rect) -> bool:
        return self.surface.get_rect().colliderect(rect)

    def to_local(self, point: Point) -> Vector2:
        return Vector2(point)

    def to_world(self, point: Point) -> Vector2:
        return Vector2(point)

    def screen_to_world(self, point: Point, viewport_index: int = 0) -> Vector2:
        return Vector2(point)

    def screen_to_world_clamped(
        self, point: Point, viewport_index: int = 0
    ) -> Vector2 | None:
        return Vector2(point)
