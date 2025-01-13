from __future__ import annotations

import typing

import pygame


if typing.TYPE_CHECKING:
    from . import Container
    from .enums import Layer
    from pygame import Surface, Rect
    from pygame.typing import Point


from .renderable import Renderable


class StaticDecor(Renderable):

    def __init__(
        self,
        display_surface: Surface,
        position: Point = (0, 0),
        container: Container = None,
        enabled=True,
        layer: Layer = None,
        draw_index=0,
    ) -> None:
        super().__init__(container, enabled, layer, draw_index)
        self.display_surface = display_surface
        self.position = pygame.Vector2(position)

    def get_rect(self) -> Rect:
        rect = self.display_surface.get_rect()
        rect.center = self.position
        return rect

    def render(self, delta_time: float) -> pygame.Surface:
        return self.display_surface
