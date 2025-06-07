from __future__ import annotations

from typing import cast, TYPE_CHECKING

from ..types import Component, HasTexture

if TYPE_CHECKING:
    from .render_texture import RenderTexture


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
