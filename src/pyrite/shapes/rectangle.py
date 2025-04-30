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

    def get_vertices(self) -> tuple[Vector2]:
        scalar = (self._width, self._height)
        return (
            self._vertices[0].elementwise() * scalar,
            self._vertices[1].elementwise() * scalar,
            self._vertices[3].elementwise() * scalar,
            self._vertices[4].elementwise() * scalar,
        )
