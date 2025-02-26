from __future__ import annotations

from abc import ABC, abstractmethod

import typing

# import pygame
from pygame import Rect, Vector2


if typing.TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any, TextIO
    from . import Container
    from .enums import Layer, Anchor
    from pygame import Surface
    from pygame.typing import Point


from .renderable import Renderable

from .enums import AnchorPoint


class SpriteMap(ABC):
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


class RowColumnSpriteMap(SpriteMap):
    """
    Version of SpriteMap that uses rows and columns and a constant size for each
    sprite.

    Takes keys as tuples of row, column
    """

    def __init__(self, number_rows: int, number_columns, sprite_size: Point) -> None:
        sprite_width, sprite_height = sprite_size
        self._map = [
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
        return self._map[row][column]


class StringSpriteMap(SpriteMap):
    """
    Version of SpriteMap that takes a string key dictionary.
    """

    def __init__(self, string_dict: dict[str, Rect]) -> None:
        self._map = string_dict

    @staticmethod
    def from_file(spritesheet_map_file: TextIO, decoder: Callable) -> StringSpriteMap:
        """
        Creates a StringSpriteMap from a file, using a supplied decoder function.
        The decoder must take a file-like object, and return a dictionary with string
        keys and pygame rectangles as values.

        :param spritesheet_map_file: File or file-like object from which the decoder
        will convert into a dict
        :param decoder: A callable that can read the specified file and turn it into a
        dict.
        :return: A StringSpriteMap based on the data from the supplied file.
        """

        map_dict = decoder(spritesheet_map_file)
        return StringSpriteMap(map_dict)

    def get(self, key: str) -> Rect:
        return self.get(key)


class SpriteSheet(Renderable):

    def __init__(
        self,
        sprite_sheet: Surface,
        sprite_map: SpriteMap,
        position: Point = (0, 0),
        anchor: Anchor = AnchorPoint.CENTER,
        start_state: Any = None,
        container: Container = None,
        enabled=True,
        layer: Layer = None,
        draw_index=0,
    ) -> None:
        super().__init__(container, enabled, layer, draw_index)
        self._sprite_sheet = sprite_sheet
        self.sprite_map = sprite_map
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
        self.surface = self._sprite_sheet.subsurface(self.sprite_map.get(state_key))

    def get_rect(self) -> Rect:
        rect = self.surface.get_rect()
        self.anchor.anchor_rect_ip(rect, self.position)
        return rect

    def render(self, delta_time: float) -> Surface:
        return self.surface
