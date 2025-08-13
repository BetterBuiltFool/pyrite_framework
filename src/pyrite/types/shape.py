from __future__ import annotations

from typing import TYPE_CHECKING

import pymunk

from pygame import Rect

if TYPE_CHECKING:
    from ..physics import RigidbodyComponent


class Shape[ShapeT: pymunk.Shape]:

    def __init__(self) -> None:
        self._rigidbody: RigidbodyComponent | None
        self._shape: ShapeT

    @property
    def area(self) -> float:
        return self._shape.area

    @property
    def bounding_box(self) -> Rect:
        bb = self._shape.bb
        left, top, right, bottom = bb.left, bb.top, bb.right, bb.bottom
        width = right - left
        height = top - bottom
        return Rect(left, top, width, height)
