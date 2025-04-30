from __future__ import annotations

import math

from pygame import Vector2

from ..transform import Transform
from ..types.shape import Shape


_vertical_axis = Vector2(0, 1)


class Stadium(Shape):

    def __init__(self, radius: float, height: float) -> None:
        self.radius = radius
        self.height = height

    def get_furthest_vertex(self, vector: Vector2, transform: Transform) -> Vector2:
        # Rotate and scale vector by transform data
        # normalize vector
        vector = self._prescale_vector(vector, transform)
        # Find the farthest point of the shape (In this case, it's now a circle)
        origin = vector * _vertical_axis
        y_offset = math.copysign(self.height / 2, origin)
        point = Vector2(0, y_offset) + (self.radius * vector)
        # Add the position component of transform
        point = point.elementwise() * transform.scale
        point = point.rotate(transform.rotation)
        point += transform.position
        # return position
        return point

    def get_vertices(self) -> tuple[Vector2]:
        # Critical Points: Foci, ends of side segments
        subheight = self.height / 2
        radius = self.radius
        return (
            Vector2(0, subheight),
            Vector2(radius, subheight),
            Vector2(radius, -subheight),
            Vector2(0, -subheight),
            Vector2(-radius, -subheight),
            Vector2(-radius, subheight),
        )
