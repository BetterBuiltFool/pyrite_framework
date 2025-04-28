from __future__ import annotations

from pygame import Vector2

from ..transform import Transform

from ..types.shape import Shape, DIRECTIONS


class Ellipse(Shape):

    def __init__(self, radius: float) -> None:
        self.radius = Vector2(radius)

    def _get_extents(self, transform: Transform) -> dict[str, Vector2]:
        extents: dict[str, Vector2] = {}
        for direction, vector in DIRECTIONS.items():
            furthest_point = self.get_furthest_vertex(vector, transform)
            extents.update({direction: furthest_point})
        return extents

    def get_furthest_vertex(self, vector: Vector2, transform: Transform) -> Vector2:
        # Rotate and scale vector by transform data
        # normalize vector
        vector = self._prescale_vector(vector, transform)
        # Find the farthest point of the shape (In this case, it's now a circle)
        point = vector.elementwise() * self.radius
        # Add the position component of transform
        point = point.elementwise() * transform.scale
        point = point.rotate(transform.rotation)
        point += transform.position
        # return position
        return point
