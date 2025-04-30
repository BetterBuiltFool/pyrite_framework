from __future__ import annotations

from pygame import Vector2

from ..transform import Transform

from ..types.shape import Shape


class Ellipse(Shape):

    def __init__(self, radius: float) -> None:
        self.radius = Vector2(radius)

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
