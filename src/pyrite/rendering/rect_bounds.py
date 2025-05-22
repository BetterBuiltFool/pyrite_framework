from __future__ import annotations

from typing import TYPE_CHECKING


from ..types.bounds import CullingBounds
from ..cuboid import Cuboid

if TYPE_CHECKING:
    from pygame import Rect


class RectBounds(CullingBounds):
    """
    Bounds described by an axis-aligned rectangle on the xy-plane.
    """

    __slots__ = ("rect",)

    def __init__(self, rect: Rect) -> None:
        self.rect = rect

    def get_volume(self) -> Cuboid:
        rect = self.rect
        return Cuboid(rect.left, rect.top, 0, rect.width, rect.height, 0)

    def get_rect(self) -> Rect:
        return self.rect
