from __future__ import annotations

from abc import ABC, abstractmethod

import typing

import pygame


if typing.TYPE_CHECKING:
    from typing import Any
# from . import Container
# from .enums import Layer, Anchor
# from pygame import Surface, Rect
# from pygame.typing import Point


from .renderable import Renderable

# from .enums import AnchorPoint


class StateDict(ABC):
    """
    A dictionary of rects for getting the subsurfaces for a spritesheet.
    """

    @abstractmethod
    def get(self, key: Any) -> pygame.Rect:
        """
        Returns a rect matching the provided key.

        :param key: Key values for the rect. Typing varies by implementation.
        :return: A rectangle representing the subsurface of the spritesheet.
        """
        pass


class SpriteSheet(Renderable):

    pass
