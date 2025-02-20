from __future__ import annotations

from abc import ABC, abstractmethod

import typing

# import pygame
from pygame import Rect, Vector2


if typing.TYPE_CHECKING:
    from typing import Any
    from . import Container
    from .enums import Layer, Anchor
    from pygame import Surface
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


class RowColumnStateDict(StateDict):
    """
    Version of state dict that uses rows and columns and a constant size for each
    sprite.

    Takes keys as tuples of row, column
    """

    def __init__(self, number_rows: int, number_columns, sprite_size: Point) -> None:
        sprite_width, sprite_height = sprite_size
        self._state = [
            [
                Rect(
                    column * sprite_width,
                    row * sprite_height,
                    sprite_width,
                    sprite_height,
                )
                for column in range(number_columns)
            ]
            for row in range(number_rows)
        ]
        self.sprite_size = sprite_size

    def get(self, key: tuple[int, int]) -> Rect:
        if key is None:
            key = (0, 0)
        row = key[0]
        column = key[1]
        return self._state[row][column]


class SpriteSheet(Renderable):

    def __init__(
        self,
        state_dict: StateDict,
        position: Point,
        anchor: Anchor = AnchorPoint.CENTER,
        start_state: Any = None,
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

        self._state = None
        self.state = start_state

    @property
    def state(self) -> Any:
        return self._state

    @state.setter
    def state(self, state_key: Any):
        self._state = state_key
        self.surface = self.state_dict.get(state_key)

    def get_rect(self) -> Rect:
        rect = self.surface.get_rect()
        self.anchor.anchor_rect_ip(rect, self.position)
        return rect

    def render(self, delta_time: float) -> Surface:
        return self.surface
