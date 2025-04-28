from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING
from pygame import Vector2

from ..transform import Transform

from ..types.shape import Shape, DIRECTIONS

if TYPE_CHECKING:
    pass


def _get_furthest(direction: Vector2, point_a: Vector2, point_b: Vector2) -> Vector2:
    a = point_a * direction
    b = point_b * direction
    return point_a if a > b else point_b


class Polygon(Shape):

    def __init__(self, vertices: Sequence[Vector2]) -> None:
        self._vertices = list(vertices)

    def _get_extents(self, transform: Transform) -> dict[str, Vector2]:
        vertices = self.get_vertices()
        initial_vert = vertices[0].rotate(-transform.rotation)
        extents: dict[str, Vector2] = {
            "up": initial_vert,
            "right": initial_vert,
            "down": initial_vert,
            "left": initial_vert,
        }
        for vertex in vertices:
            transformed_vertex = vertex.rotate(-transform.rotation)
            for extent_key, extent_value in extents.items():
                extents[extent_key] = _get_furthest(
                    DIRECTIONS[extent_key], extent_value, transformed_vertex
                )
        return extents

    def get_furthest_vertex(self, vector: Vector2, transform: Transform) -> Vector2:
        pass

    def get_vertices(self) -> list[Vector2]:
        return self._vertices
