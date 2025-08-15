from __future__ import annotations

from typing import TYPE_CHECKING

from pygame import Vector2
import pymunk

from ..types.shape import Shape
from ..utils import point_to_tuple

if TYPE_CHECKING:
    from collections.abc import Sequence

    from pygame import Rect
    from pygame.typing import Point

    from . import ColliderComponent
    from ..types import TransformLike


class Circle(Shape[pymunk.Circle]):

    def __init__(
        self, collider: ColliderComponent | None, radius: float, offset: Point = (0, 0)
    ) -> None:
        super().__init__(collider)

        self._shape = pymunk.Circle(None, radius, point_to_tuple(offset))

    # TODO: Add access to unsafe setters?

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


class Polygon(Shape[pymunk.Poly]):

    def __init__(
        self,
        collider: ColliderComponent | None,
        verts: Sequence[Point],
        transform: TransformLike | None = None,
        radius: float = 0,
    ) -> None:
        super().__init__(collider)
        vert_transform: pymunk.Transform | None = None
        if transform:
            vert_transform = (
                pymunk.Transform.translation(transform.position.x, transform.position.y)
                .rotated(transform.rotation)
                .scaled(transform.scale.x)  # pymunk can only handle uniform scaling.
            )
        self._shape = pymunk.Poly(
            None, [point_to_tuple(vert) for vert in verts], vert_transform, radius
        )

    def get_vertices(self) -> list[Vector2]:
        """
        Returns the relative positions of each vertex in the shape.
        """
        return [Vector2(vert) for vert in self._shape.get_vertices()]

    @staticmethod
    def make_box(
        collider: ColliderComponent | None, size: Point = (10, 10), radius: float = 0
    ) -> Polygon:
        width, height = size
        verts = [
            (-width / 2, height / 2),
            (width / 2, height / 2),
            (width / 2, -height / 2),
            (-width / 2, -height / 2),
        ]
        return Polygon(collider, verts, None, radius)

    @staticmethod
    def make_box_from_rect(
        collider: ColliderComponent | None, rect: Rect, radius: float = 0
    ) -> Polygon:
        verts = [rect.topleft, rect.topright, rect.bottomright, rect.bottomleft]
        return Polygon(collider, verts, None, radius)
