from __future__ import annotations

from abc import ABC, abstractmethod

import typing

# import pygame
from pygame import Vector2
from pygame.rect import Rect as Rect
from pygame.surface import Surface as Surface


if typing.TYPE_CHECKING:
    from typing import Any
    from . import Container
    from .enums import Layer, Anchor
    from pygame import Rect, Surface
    from pygame.typing import Point


from .renderable import Renderable

from .enums import AnchorPoint


class StateDict(ABC):
    """
    A dictionary of rects for getting the subsurfaces for a spritesheet.
    """

    @abstractmethod
    def get(self, key: Any) -> Rect:
        """
        Returns a rect matching the provided key.

        :param key: Key values for the rect. Typing varies by implementation.
        :return: A rectangle representing the subsurface of the spritesheet.
        """
        pass


class SpriteSheet(Renderable):

    def __init__(
        self,
        state_dict: StateDict,
        position: Point,
        anchor: Anchor = AnchorPoint.CENTER,
        container: Container = None,
        enabled=True,
        layer: Layer = None,
        draw_index=0,
    ) -> None:
        super().__init__(container, enabled, layer, draw_index)
        self.state_dict = state_dict
        self.position = Vector2(position)
        self.anchor = anchor
        self.surface: Surface = None

    def get_rect(self) -> Rect:
        rect = self.surface.get_rect()
        self.anchor.anchor_rect_ip(rect, self.position)
        return rect

    def render(self, delta_time: float) -> Surface:
        return self.surface
