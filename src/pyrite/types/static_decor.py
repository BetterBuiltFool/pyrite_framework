from __future__ import annotations

import typing
import warnings

import pygame


if typing.TYPE_CHECKING:
    from . import Container
    from ..enum import Layer, Anchor
    from pygame import Surface, Rect
    from pygame.typing import Point


from .renderable import Renderable
from ..enum import AnchorPoint

first_creation = True


def warn_deprecated():
    global first_creation
    if first_creation:
        warnings.warn(
            "StaticDecor is deprecated. Use Sprite instead.", DeprecationWarning
        )
        first_creation = False


class StaticDecor(Renderable):
    """
    DEPRECATED

    A basic renderable with a world position and a surface to display.
    Has no behavior, just renders.
    """

    def __init__(
        self,
        display_surface: Surface,
        position: Point = (0, 0),
        anchor: Anchor = AnchorPoint.CENTER,
        container: Container = None,
        enabled=True,
        layer: Layer = None,
        draw_index=0,
    ) -> None:
        """
        DEPRECATED

        A Decor object with no behavior. Renders a surface based on its position.

        :param display_surface: The image or surface to be shown.
        :param position: Location of the Decor object, in world space,
        defaults to (0, 0)
        :param anchor: AnchorPoint that determines where on the object the position
        references, defaults to Anchor.CENTER
        :param container: Container object for the renderable, defaults to None
        :param enabled: Whether or not the object should be active immediately upon
        spawn, defaults to True
        :param layer: Render layer to which the object belongs, defaults to None
        :param draw_index: Draw order for the renderable, defaults to 0
        """
        warn_deprecated()
        super().__init__(container, enabled, layer, draw_index)
        self.display_surface = display_surface
        self.position = pygame.Vector2(position)
        self.anchor = anchor

    def get_rect(self) -> Rect:
        rect = self.display_surface.get_rect()
        self.anchor.anchor_rect_ip(rect, self.position)
        return rect

    def render(self, delta_time: float) -> pygame.Surface:
        return self.display_surface
