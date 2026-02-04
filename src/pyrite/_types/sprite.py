from __future__ import annotations

from typing import TYPE_CHECKING

from pyrite._types.renderable import Renderable

if TYPE_CHECKING:
    from pygame import Surface, Vector2
    from pygame.typing import Point

    from pyrite.enum import Anchor
    from pyrite.transform import TransformComponent


class Sprite(Renderable):

    anchor: Anchor
    transform: TransformComponent

    @property
    def position(self) -> Vector2: ...

    @position.setter
    def position(self, position: Point): ...

    @property
    def flip_x(self) -> bool:
        """
        Shows if the image is set to be flipped along the x axis.
        """
        ...

    @flip_x.setter
    def flip_x(self, flip_x: bool):
        """
        Sets the sprite to be flipped along the x axis.
        Note: setting this directly will not automatically flip the display. Use
        set_surface() for that, or call _force_update_surface() after setting the flip
        parameters.

        :param flip_x: Boolean determining whether to flip the sprite image.
        """
        ...

    @property
    def flip_y(self) -> bool:
        """
        Shows if the image is set to be flipped along the y axis.
        """
        ...

    @flip_y.setter
    def flip_y(self, flip_y: bool):
        """
        Sets the sprite to be flipped along the y axis.
        Note: setting this directly will not automatically flip the display. Use
        set_surface() for that, or call _force_update_surface() after setting the flip
        parameters.

        :param flip_y: Boolean determining whether to flip the sprite image.
        """
        ...

    @property
    def is_dirty(self) -> bool: ...

    @is_dirty.setter
    def is_dirty(self, is_dirty: bool): ...

    def set_surface(
        self,
        sprite_image: Surface | None = None,
        flip_x: bool | None = None,
        flip_y: bool | None = None,
    ):
        """
        Changes the sprite's display to match the given properties.
        If any parameter is None, it uses the sprite's current setting.

        :param sprite_image: The raw surface being used, defaults to None
        :param flip_x: Whether to flip along the x axis, defaults to None
        :param flip_y: Whether to flip along the y axis, defaults to None
        """
        ...

    def get_surface(self) -> Surface:
        """
        Returns the reference surface used by the sprite.
        """
        ...
