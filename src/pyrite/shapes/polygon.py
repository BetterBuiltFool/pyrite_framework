from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING
from pygame import Vector2

from ..types.shape import Shape

if TYPE_CHECKING:
    from ..transform import Transform


def _get_furthest(direction: Vector2, point_a: Vector2, point_b: Vector2) -> Vector2:
    a = point_a * direction
    b = point_b * direction
    return point_a if a > b else point_b


class Polygon(Shape):

    def __init__(self, vertices: Sequence[Vector2]) -> None:
        self._vertices = list(vertices)

    def get_furthest_vertex(self, vector: Vector2, transform: Transform) -> Vector2:
        # Translate the vector into unit space
        vector = self._prescale_vector(vector, transform)
        furthest: Vector2 = None
        distance = 0
        for vertex in self.get_vertices():
            new_distance = vertex * vector
            if new_distance > distance:
                distance = new_distance
                furthest = vertex

        furthest = furthest.elementwise() * transform.scale
        furthest = furthest.rotate(transform.rotation)
        furthest += transform.position

        return furthest

    def get_vertices(self) -> list[Vector2]:
        return self._vertices
