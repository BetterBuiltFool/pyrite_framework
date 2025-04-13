from __future__ import annotations

import typing

import pygame


if typing.TYPE_CHECKING:
    from . import Container
    from ..transform.transform import Transform
    from .enums import Layer, Anchor
    from pygame import Surface, Rect, Vector2
    from pygame.typing import Point


from .renderable import Renderable
from .enums import AnchorPoint

from ..transform import transform


class Sprite(Renderable):
    """
    A basic renderable with a world position and a surface to display.
    """

    def __init__(
        self,
        display_surface: Surface,
        position: Point = (0, 0),
        local_transform: Transform = None,
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
        self._reference_image = display_surface
        self.display_surface = display_surface
        if local_transform is not None:
            if isinstance(local_transform, transform.TransformComponent):
                # If we're being passed something else's transform,
                # we'll just use that instead.
                self.transform = local_transform
            else:
                self.transform = transform.from_transform(self, local_transform)
        else:
            self.transform = transform.from_attributes(self, position)
        # self.position = pygame.Vector2(position)
        self.anchor = anchor

        # Clients can update these easily enough.
        self._flip_x = False
        self._flip_y = False

        self._is_dirty = True

    @property
    def position(self) -> Vector2:
        return self.transform.position

    @position.setter
    def position(self, new_position: Point):
        self.transform.position = new_position

    @property
    def flip_x(self) -> bool:
        """
        Shows if the image is set to be flipped along the x axis.
        """
        return self._flip_x

    @flip_x.setter
    def flip_x(self, flag: bool):
        """
        Sets the sprite to be flipped along the x axis.
        Note: setting this directly will not automatically flip the display. Use
        set_surface() for that, or call _force_update_surface() after setting the flip
        parameters.

        :param flag: Boolean determining whether to flip the sprite image.
        """
        self._flip_x = flag

    @property
    def flip_y(self) -> bool:
        """
        Shows if the image is set to be flipped along the y axis.
        """
        return self._flip_y

    @flip_y.setter
    def flip_y(self, flag: bool):
        """
        Sets the sprite to be flipped along the y axis.
        Note: setting this directly will not automatically flip the display. Use
        set_surface() for that, or call _force_update_surface() after setting the flip
        parameters.

        :param flag: Boolean determining whether to flip the sprite image.
        """
        self._flip_y = flag

    def set_surface(
        self, sprite_image: Surface = None, flip_x: bool = None, flip_y: bool = None
    ):
        """
        Changes the sprite's display to match the given properties.
        If any parameter is None, it uses the sprite's current setting.

        :param sprite_image: The raw surface being used, defaults to None
        :param flip_x: Whether to flip along the x axis, defaults to None
        :param flip_y: Whether to flip along the y axis, defaults to None
        """
        sprite_image = (
            sprite_image if sprite_image is not None else self._reference_image
        )
        flip_x = flip_x if flip_x is not None else self.flip_x
        flip_y = flip_y if flip_y is not None else self.flip_y

        self.flip_x, self.flip_y = flip_x, flip_y

        self._reference_image = sprite_image

        self._is_dirty = True

    def _force_update_surface(self) -> Surface:
        new_surface = pygame.transform.flip(
            self._reference_image, self.flip_x, self.flip_y
        )
        self._is_dirty = False

        # FIXME This really only works for centered renderables

        new_surface = pygame.transform.scale_by(new_surface, self.transform.world_scale)

        new_surface = pygame.transform.rotate(
            new_surface, self.transform.world_rotation
        )

        self.transform._dirty = False

        return new_surface

    def get_rect(self) -> Rect:
        rect = self.display_surface.get_rect()
        self.anchor.anchor_rect_ip(rect, self.transform.world_position)
        return rect

    def render(self, delta_time: float) -> pygame.Surface:
        if self._is_dirty or self.transform._dirty:
            self.display_surface = self._force_update_surface()
        return self.display_surface
