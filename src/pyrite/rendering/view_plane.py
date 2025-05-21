from __future__ import annotations

from typing import TYPE_CHECKING


from ..types.view_bounds import CameraViewBounds

if TYPE_CHECKING:
    from pygame import Rect
    from ..types.bounds import CullingBounds


class ViewPlane(CameraViewBounds):

    def __init__(self, view_rect: Rect) -> None:
        self.view_rect = view_rect

    def contains(self, bounds: CullingBounds) -> bool:
        # 'flatten' will convert the bounds to a 2D object we can handle.
        return self.view_rect.colliderect(bounds.flatten())
