from __future__ import annotations

import typing

import pygame


if typing.TYPE_CHECKING:
    from . import Container
    from .enums import Layer, Anchor
    from pygame import Surface, Rect
    from pygame.typing import Point


from .renderable import Renderable
from .enums import AnchorPoint


class Sprite(Renderable):
    """
    A basic renderable with a world position and a surface to display.
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
        A basic renderable that displays a surface at a world position.

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
        super().__init__(container, enabled, layer, draw_index)
        self.display_surface = display_surface
        self.position = pygame.Vector2(position)
        self.anchor = anchor

        # Clients can update these easily enough.
        self._flip_x = False
        self._flip_y = False

    @property
    def flip_x(self) -> bool:
        return self._flip_x

    @flip_x.setter
    def flip_x(self, flag: bool):
        self._flip_x = flag

    @property
    def flip_y(self) -> bool:
        return self._flip_y

    @flip_y.setter
    def flip_y(self, flag: bool):
        self.flip_y = flag

    def set_surface(self, sprite_image: Surface, flip_x=None, flip_y=None):
        flip_x = flip_x if flip_x is not None else self.flip_x
        flip_y = flip_y if flip_y is not None else self.flip_y

        self.flip_x, self.flip_y = flip_x, flip_y

        new_surface = pygame.transform.flip(sprite_image, flip_x, flip_y)

        self.display_surface = new_surface

    def get_rect(self) -> Rect:
        rect = self.display_surface.get_rect()
        self.anchor.anchor_rect_ip(rect, self.position)
        return rect

    def render(self, delta_time: float) -> pygame.Surface:
        return self.display_surface
