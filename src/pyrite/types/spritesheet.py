from __future__ import annotations

from abc import ABC, abstractmethod

import typing

import pygame
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
    def from_file(
        spritesheet_map_file: TextIO, decoder: Callable = None
    ) -> StringSpriteMap:
        """
        Creates a StringSpriteMap from a text file, using a supplied decoder function.
        The decoder must take a file-like object, and return a dictionary with string
        keys and pygame rectangles as values.

        The default decoder function assumes a layout where each subrect is on its own
        line, with no blank lines, and each line takes the form of "[state] = x y w h"

        :param spritesheet_map_file: File or file-like object from which the decoder
        will convert into a dict
        :param decoder: A callable that can read the specified file and turn it into a
        dict.
        :return: A StringSpriteMap based on the data from the supplied file.
        """
        if not decoder:

            def decoder(sprite_map_file: TextIO) -> dict[str, Rect]:
                states: dict[str, Rect] = {}
                for line in sprite_map_file.readlines():
                    key, value = line.split("=")
                    key = key.strip(" ")
                    value = value.strip("\n")
                    value = value.lstrip()
                    values = [int(subvalue) for subvalue in value.split(" ")]
                    states.update({key: Rect(*values)})
                return states

        map_dict = decoder(spritesheet_map_file)
        return StringSpriteMap(map_dict)

    def get(self, key: str) -> Rect:
        return self._map.get(key)


class SpriteSheet(Renderable):
    """
    A renderable that can display subsections of a larger surface.
    Useful for animations, or otherwise collecting multiple images
    into one larger surface.

    Requires a SpriteMap.
    """

    def __init__(
        self,
        reference_sprite: Surface,
        sprite_map: SpriteMap,
        position: Point = (0, 0),
        start_state: Any = None,
        anchor: Anchor = AnchorPoint.CENTER,
        container: Container = None,
        enabled=True,
        layer: Layer = None,
        draw_index=0,
    ) -> None:
        """
        Creates a new Spritesheet renderable.

        :param reference_sprite: The reference surface containing all of the subsurfaces
        needed. As a reference, can be shared by multiple sprite sheets.
        :param sprite_map: A SpriteMap of any type, containing the Rect coordinates of
        all of the subsurfaces.
        :param position: The SpriteSheet's position in world space, defaults to (0, 0)
        :param start_state: The initial state of the SpriteSheet. None allows the
        SpriteMap to choose. Defaults to None.
        :param anchor: Determines where on the subsurface the position references,
        defaults to AnchorPoint.CENTER
        :param container: Object containing the renderable, defaults to None
        :param enabled: Whether the renderable should be rendered, defaults to True
        :param layer: Layer in the layer queue the renderable will be drawn in,
        defaults to None
        :param draw_index: Relative order the renderable will be drawn in, defaults to 0
        """
        super().__init__(container, enabled, layer, draw_index)
        self._reference_sprite = reference_sprite
        self.sprite_map = sprite_map
        self.position = Vector2(position)
        self.anchor = anchor
        self.surface: Surface = None

        self.flip_x = False
        self.flip_y = False

        self._state = None
        self.state = start_state

    @property
    def state(self) -> Any:
        """
        A value used by the SpriteMap to select the subsurface to be displayed.

        Type matches the type of the key used by the chosen SpriteMap.
        """
        return self._state

    @state.setter
    def state(self, state_key: Any):
        self._state = state_key
        subsurface = self._reference_sprite.subsurface(self.sprite_map.get(state_key))
        self._set_surface(subsurface, self.flip_x, self.flip_y)

    def _set_surface(self, subsurface, flip_x, flip_y):
        self.surface = pygame.transform.flip(subsurface, flip_x, flip_y)

    def get_rect(self) -> Rect:
        rect = self.surface.get_rect()
        self.anchor.anchor_rect_ip(rect, self.position)
        return rect

    def render(self, delta_time: float) -> Surface:
        return self.surface
