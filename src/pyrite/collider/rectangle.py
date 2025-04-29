from __future__ import annotations

from pygame import Vector2

from .polygon import Polygon


class Rectangle(Polygon):
    _vertices = (
        Vector2(0.5, 0.5),
        Vector2(-0.5, 0.5),
        Vector2(-0.5, -0.5),
        Vector2(0.5, -0.5),
    )

    def __init__(self, width: float, height: float) -> None:
        self._width = width
        self._height = height

    def get_vertices(self) -> list[Vector2]:
        return [
            vertex.elementwise() * (self._width, self._height)
            for vertex in self._vertices
        ]
