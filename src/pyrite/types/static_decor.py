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
    """
    A basic renderable with a world position and a surface to display.
    Has no behavior, just renders.
    """

    def __init__(
        self,
        display_surface: Surface,
        position: Point = (0, 0),
        container: Container = None,
        enabled=True,
        layer: Layer = None,
        draw_index=0,
    ) -> None:
        """
        A Decor object with no behavior. Renders a surface based on its position.

        :param display_surface: The image or surface to be shown.
        :param position: Location of the Decor object, in world space,
        defaults to (0, 0)
        :param container: Container object for the renderable, defaults to None
        :param enabled: Whether or not the object should be active immediately upon
        spawn, defaults to True
        :param layer: Render layer to which the object belongs, defaults to None
        :param draw_index: Draw order for the renderable, defaults to 0
        """
        super().__init__(container, enabled, layer, draw_index)
        self.display_surface = display_surface
        self.position = pygame.Vector2(position)

    def get_rect(self) -> Rect:
        rect = self.display_surface.get_rect()
        rect.center = self.position
        return rect

    def render(self, delta_time: float) -> pygame.Surface:
        return self.display_surface