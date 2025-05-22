from __future__ import annotations

import math
from typing import TYPE_CHECKING

from pygame import Vector2

from ..types.bounds import CullingBounds
from ..cuboid import Cuboid
from pygame import Rect

if TYPE_CHECKING:
    from pygame.typing import Point


def rotate_rect(rect: Rect, angle: float, pivot: Point) -> Rect:
    """
    Generates a Rect that describes the bounding box of a rotated Rect.

    :param rect: The initial rect, assumed to be axis-aligned.
    :param angle: The target angle the rect should be at.
    :param pivot: Offset from from center of the rect.
    :return: The bounding box of the rotated rect.
    """
    pivot = Vector2(pivot)

    center = rect.center
    new_center = center + pivot

    rad_angle = math.radians(angle)

    new_height = rect.height * math.cos(rad_angle) + rect.width * math.sin(rad_angle)
    new_width = rect.width * math.cos(rad_angle) + rect.height * math.sin(rad_angle)
    new_rect = Rect(0, 0, new_width, new_height)

    rotated_pivot = pivot.rotate(angle)

    new_rect.center = new_center - rotated_pivot

    return new_rect


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
