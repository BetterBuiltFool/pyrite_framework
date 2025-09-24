from __future__ import annotations

from typing import cast, TYPE_CHECKING

from pygame import Rect, Surface

from pyrite._component.component import BaseComponent as Component
from pyrite._types.protocols import HasTexture

if TYPE_CHECKING:
    from pygame.typing import Point


class RenderTexture:
    """
    A special RenderTarget that receives rendered images from a camera.
    """

    def __init__(self, size: Point) -> None:
        self.render_surface = self._resize_surface(size)
        self._crop = False

    @property
    def crop(self) -> bool:
        """
        Determines if the rendering should be cropped or not.
        If False, the rendering will be scaled to fit the target.
        """
        return self._crop

    @crop.setter
    def crop(self, crop: bool):
        self._crop = crop

    def get_target_surface(self) -> Surface:
        """
        Gets the surface to be drawn to.
        """
        return self.render_surface

    def get_target_rect(self) -> Rect:
        """
        Gets the Rect that represents the surface space of the RenderTarget.
        """
        return self.render_surface.get_rect()

    def resize_surface(self, size: Point):
        """
        Updates the surface to the new size. Any render data will be lost.

        :param size: A point representing the new size of the surface
        """
        self.render_surface = self._resize_surface(size)

    def _resize_surface(self, size: Point) -> Surface:
        return Surface(size)


class RenderTextureComponent(Component):
    """
    Special component for sprites and sprite-like objects. Automatically updates the
    object's texture to the assigned rendertexture, and ensures it is redrawn to update.
    """

    def __init__(self, owner: HasTexture, render_texture: RenderTexture) -> None:
        super().__init__(owner)
        self.render_texture = render_texture

    def update_texture(self):
        owner = cast(HasTexture, self.owner)
        owner.texture = self.render_texture.get_target_surface()
        owner.is_dirty = True
