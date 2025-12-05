from __future__ import annotations

from typing import TYPE_CHECKING

from pygame import Vector2
import pymunk

from pyrite._types.shape import Shape
from pyrite.utils import point_to_tuple

if TYPE_CHECKING:
    from collections.abc import Sequence

    from pygame import Rect
    from pygame.typing import Point

    from pyrite._component.collider_component import ColliderComponent
    from pyrite._types.protocols import HasTransformAttributes


class Circle(Shape[pymunk.Circle]):
    """
    Basic circle shape.
    """

    def __init__(
        self, collider: ColliderComponent | None, radius: float, offset: Point = (0, 0)
    ) -> None:
        super().__init__(collider, pymunk.Circle(None, radius, point_to_tuple(offset)))

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
    """
    Shape built out of discrete vertices.

    For rectangular shapes, you can use the shortcut of Polygon.make_box() or
    Polygon.make_box_from_rect()
    """

    def __init__(
        self,
        collider: ColliderComponent | None,
        verts: Sequence[Point],
        transform: HasTransformAttributes | None = None,
        radius: float = 0,
    ) -> None:
        vert_transform: pymunk.Transform | None = None
        if transform:
            vert_transform = (
                pymunk.Transform.translation(transform.position.x, transform.position.y)
                .rotated(transform.rotation)
                .scaled(transform.scale.x)  # pymunk can only handle uniform scaling.
            )
        super().__init__(
            collider,
            pymunk.Poly(
                None, [point_to_tuple(vert) for vert in verts], vert_transform, radius
            ),
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
        """
        Creates a box-shaped polygon collider based on the provided size.

        Size is taken in width, height order.

        :param collider: The collider component that the shape belongs to, or None.
        :param size: A tuple of numbers describing the width and height of the box,
            defaults to (10, 10)
        :param radius: Optional bevel to make sliding along surfaces easier, defaults
            to 0
        :return: The completed Polygon.
        """
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
        """
        Creates a box-shaped polygon collider based on the provided rectangle. The rect
        will be in local space.

        :param collider: The collider component that the shape belongs to, or None.
        :param rect: A rect describing the width, height, and top left corner of the
            new box.
        :param radius: Optional bevel to make sliding along surfaces easier, defaults
            to 0
        :return: The completed Polygon.
        """
        verts = [rect.topleft, rect.topright, rect.bottomright, rect.bottomleft]
        return Polygon(collider, verts, None, radius)


class Segment(Shape[pymunk.Segment]):
    """
    Simple linear collider, good for making floors and walls.

    Ensure that the radius is thick enough to prevent passthrough by speedy objects.
    """

    def __init__(
        self,
        collider: ColliderComponent | None,
        a: Point,
        b: Point,
        radius: float,
    ) -> None:
        super().__init__(
            collider, pymunk.Segment(None, point_to_tuple(a), point_to_tuple(b), radius)
        )

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
