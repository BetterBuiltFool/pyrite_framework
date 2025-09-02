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
        self._shapes[self._shape] = self

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
        self._shapes[self._shape] = self

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


class Segment(Shape[pymunk.Segment]):

    def __init__(
        self,
        collider: ColliderComponent | None,
        a: Point,
        b: Point,
        radius: float,
    ) -> None:
        super().__init__(collider)

        self._shape = pymunk.Segment(None, point_to_tuple(a), point_to_tuple(b), radius)
        self._shapes[self._shape] = self

    @property
    def a(self) -> Vector2:
        """
        Position of the first endpoint of the segment.
        """
        return Vector2(self._shape.a)

    @a.setter
    def a(self, a: Point) -> None:
        self._shape.a = point_to_tuple(a)

    @property
    def b(self) -> Vector2:
        """
        Position of the second endpoint of the segment.
        """
        return Vector2(self._shape.b)

    @b.setter
    def b(self, b: Point) -> None:
        self._shape.b = point_to_tuple(b)

    @property
    def normal(self) -> Vector2:
        """
        The calculated normal of this segment.
        """
        return Vector2(self._shape.normal)

    def set_neighbors(
        self, prev: Segment | None = None, next: Segment | None = None
    ) -> None:
        """
        Sets the neighbors to avoid collision with 'cracks' between segments.
        """
        prev_point = prev.b if prev else self.a
        next_point = next.a if next else self.b
        self.set_neighbor_points(prev_point, next_point)

    def set_neighbor_points(self, prev: Point, next: Point) -> None:
        """
        Sets neighbors based directly on the endpoints provided.

        :param prev: A point in space that is the second endpoint of the previous
            neighbor.
        :param next: A point in space that is the first endpoint of the next neighbor.
        """
        self._shape.set_neighbors(point_to_tuple(prev), point_to_tuple(next))
