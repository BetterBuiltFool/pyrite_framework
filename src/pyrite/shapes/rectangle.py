from __future__ import annotations

from typing import TYPE_CHECKING

from pygame import draw, Surface, Vector2

from .polygon import Polygon

if TYPE_CHECKING:
    from pygame.typing import ColorLike


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
            self._vertices[2].elementwise() * scalar,
            self._vertices[3].elementwise() * scalar,
        )

    def draw(
        self,
        edge_width: int = 1,
        edge_color: ColorLike = None,
        fill_color: ColorLike = None,
    ) -> Surface:
        surface = super().draw(edge_width, edge_color, fill_color)
        if fill_color:
            surface.fill(fill_color)
        if edge_width > 0:
            draw.rect(
                surface, edge_color, (0, 0, self._width, self._height), edge_width
            )
        return surface
