from __future__ import annotations

from typing import TYPE_CHECKING
from weakref import ref

from pygame import Vector2
import pymunk

from ..types.shape import Shape
from ..utils import point_to_tuple

if TYPE_CHECKING:
    from pygame.typing import Point

    from . import ColliderComponent


class Circle(Shape[pymunk.Circle]):

    def __init__(
        self, collider: ColliderComponent | None, radius: float, offset: Point = (0, 0)
    ) -> None:
        super().__init__()
        if collider:
            self._collider = ref(collider)
        self._collider = ref(collider) if collider else None

        self._shape = pymunk.Circle(None, radius, point_to_tuple(offset))

    @property
    def radius(self) -> float:
        """
        The radius of this circle.
        """
        return self._shape.radius

    @property
    def offset(self) -> Vector2:
        """
        Offset of the shape's center from its rigidbody.
        Value is local to the body's transform.
        """
        return Vector2(self._shape.offset)
