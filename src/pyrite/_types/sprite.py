from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from pyrite._types.renderable import Renderable

if TYPE_CHECKING:
    from pygame import Surface, Vector2
    from pygame.typing import Point

    from pyrite.enum import Anchor
    from pyrite.transform import TransformComponent


class BaseSprite(Renderable):

    anchor: Anchor
    transform: TransformComponent

    @property
    @abstractmethod
    def position(self) -> Vector2: ...

    @position.setter
    @abstractmethod
    def position(self, position: Point): ...

    @property
    @abstractmethod
    def flip_x(self) -> bool:
        """
        Shows if the image is set to be flipped along the x axis.
        """
        pass

    @flip_x.setter
    @abstractmethod
    def flip_x(self, flip_x: bool):
        """
        Sets the sprite to be flipped along the x axis.
        Note: setting this directly will not automatically flip the display. Use
        set_surface() for that, or call _force_update_surface() after setting the flip
        parameters.

        :param flip_x: Boolean determining whether to flip the sprite image.
        """
        pass

    @property
    @abstractmethod
    def flip_y(self) -> bool:
        """
        Shows if the image is set to be flipped along the y axis.
        """
        pass

    @flip_y.setter
    @abstractmethod
    def flip_y(self, flip_y: bool):
        """
        Sets the sprite to be flipped along the y axis.
        Note: setting this directly will not automatically flip the display. Use
        set_surface() for that, or call _force_update_surface() after setting the flip
        parameters.

        :param flip_y: Boolean determining whether to flip the sprite image.
        """
        pass

    @property
    @abstractmethod
    def is_dirty(self) -> bool: ...

    @is_dirty.setter
    @abstractmethod
    def is_dirty(self, is_dirty: bool): ...

    @abstractmethod
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
        pass

    @abstractmethod
    def get_surface(self) -> Surface:
        """
        Returns the reference surface used by the sprite.
        """
        pass
