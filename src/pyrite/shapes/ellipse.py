from __future__ import annotations

from typing import TYPE_CHECKING

from pygame import draw, Rect, Surface, Vector2

from ..transform import Transform

from ..types.shape import Shape

if TYPE_CHECKING:
    from pygame.typing import ColorLike


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

    def draw(
        self,
        edge_width: int = 1,
        edge_color: ColorLike = None,
        fill_color: ColorLike = None,
    ) -> Surface:
        surface = super().draw(edge_width, edge_color, fill_color)
        origin = (surface.width / 2, surface.height / 2)
        fill_rect = Rect(0, 0, surface.width, surface.height)
        fill_rect.center = origin
        if fill_color is not None:
            draw.ellipse(
                surface,
                fill_color,
                fill_rect,
            )
        if edge_width > 0:
            draw.ellipse(surface, edge_color, fill_rect, width=edge_width)
        return surface

    def get_vertices(self) -> tuple[Vector2]:
        # Critical point: Origin
        return (Vector2(0, 0),)
