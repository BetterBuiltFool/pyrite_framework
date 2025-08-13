from __future__ import annotations

from typing import TYPE_CHECKING

import pymunk

if TYPE_CHECKING:
    from ..physics import RigidbodyComponent


class Shape[ShapeT: pymunk.Shape]:

    def __init__(self) -> None:
        self._rigidbody: RigidbodyComponent | None
        self._shape: ShapeT

    @property
    def area(self) -> float:
        return self._shape.area
