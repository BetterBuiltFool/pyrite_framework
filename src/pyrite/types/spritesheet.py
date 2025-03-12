from __future__ import annotations

from abc import ABC, abstractmethod

import pathlib
import typing

import pygame
from pygame import Rect, Vector2


if typing.TYPE_CHECKING:
    import os
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


class SimpleSpriteMap(SpriteMap):
    """
    Version of SpriteMap that uses rows and columns and a constant size for each
    sprite.

    sprite_size is the size of the displayed object, not the reference sheet.

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
        row, column = key
        return self._map[row][column]


class StringSpriteMap(SpriteMap):
    """
    Version of SpriteMap that takes a string key dictionary.
    TODO: Give this a better name. Don't forget to update the tests!
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

    @staticmethod
    def from_path(
        spritesheet_map_path: os.PathLike | str, decoder: Callable = None
    ) -> StringSpriteMap:

        path = pathlib.Path(spritesheet_map_path)
        with open(path) as spritemap_file:
            return StringSpriteMap.from_file(spritemap_file, decoder)

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

        self._flip_x = False
        self._flip_y = False

        self._state = None
        self.set_state(start_state)
        # self.state = start_state

    @property
    def state(self) -> Any:
        """
        A value used by the SpriteMap to select the subsurface to be displayed.

        Type matches the type of the key used by the chosen SpriteMap.
        """
        return self._state

    @property
    def flip_x(self):
        return self._flip_x

    @property
    def flip_y(self):
        return self._flip_y

    def set_state(
        self, state_key: Any = None, flip_x: bool = None, flip_y: bool = None
    ):
        """
        Updates the attributes of the spritesheet that determine the surface to be
        drawn.

        Then, updates the surface to reflect these new values.

        If a parameter is None, it will use the current value stored by the spritesheet.

        :param state_key: The key used to determine the subrect, defaults to None
        :param flip_x: Whether to flip along the x axis, defaults to None
        :param flip_y: Whether to flip along th y axis, defaults to None
        """
        self.set_state_no_update(state_key, flip_x, flip_y)

        self.force_sprite_update()

    def set_state_no_update(
        self, state_key: Any = None, flip_x: bool = None, flip_y: bool = None
    ):
        """
        Updates the attributes of the spritesheet that determine the surface to be
        drawn, but exlicitly does NOT update the current sprite.

        If a parameter is None, it will use the current value stored by the spritesheet.

        :param state_key: The key used to determine the subrect, defaults to None
        :param flip_x: Whether to flip along the x axis, defaults to None
        :param flip_y: Whether to flip along th y axis, defaults to None
        """

        self._state, self._flip_x, self._flip_y = self._validate_state(
            state_key, flip_x, flip_y
        )

    def force_sprite_update(self):
        """
        Forces the sprite to update based on the internal state parameters.
        """
        subsurface = self.get_subsurface(self._state)
        self._set_surface(subsurface, self._flip_x, self._flip_y)

    def get_subsurface(self, state_key: Any) -> Surface:
        """
        Gets a subsurface of the reference sheet based on the supplied state_key.

        If the key is invalid, returns the current surface.

        :param state_key: State value appropriate for the spritesheet's SpriteMap
        :return: The subsurface matching the state key.
        """
        rect = self.sprite_map.get(state_key)
        if rect is None:
            return self.surface
        return self._reference_sprite.subsurface(rect)

    def _validate_state(
        self, state_key: Any, flip_x: bool, flip_y: bool
    ) -> tuple[Any, bool, bool]:
        """
        Replaces any unsupplied parameter with the value stored in the spritesheet

        :param state_key: The key used to determine the subrect
        :param flip_x: Whether to flip along the x axis
        :param flip_y: Whether to flip along th y axis
        :return: A tuple containing the validate values, in order.
        """

        state_key = state_key or self.state
        flip_x = flip_x if flip_x is not None else self.flip_x
        flip_y = flip_y if flip_y is not None else self.flip_y

        return (state_key, flip_x, flip_y)

    def _set_surface(self, subsurface: Surface, flip_x: bool, flip_y: bool):
        """
        Creates a new surface from the supplied subsurface, transformed to match the
        appropriate flip settings.

        :param subsurface: Reference surface being transformed.
        :param flip_x: Whether to flip along the x axis
        :param flip_y: Whether to flip along th y axis
        """
        self.surface = pygame.transform.flip(subsurface, flip_x, flip_y)

    def get_rect(self) -> Rect:
        rect = self.surface.get_rect()
        self.anchor.anchor_rect_ip(rect, self.position)
        return rect

    def render(self, delta_time: float) -> Surface:
        return self.surface
