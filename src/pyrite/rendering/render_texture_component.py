from __future__ import annotations

from typing import TYPE_CHECKING

from ..types import Component

if TYPE_CHECKING:
    pass


class RenderTextureComponent(Component):
    """
    Special component for sprites and sprite-like objects. Automatically updates the
    object's texture to the assigned rendertexture, and ensures it is redrawn to update.
    """
