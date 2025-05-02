from __future__ import annotations

from typing import TYPE_CHECKING
from pygame import Rect, Surface, Vector2

from ..types.shape import Shape

if TYPE_CHECKING:
    from ..transform import Transform
    from pygame.typing import ColorLike


class Point(Shape):
    """
    A fixed point in space.
    Can be used statically.

    Vertices: Always (0,0)
    """

    # Point has all static methods, since it has no state. You don't need to
    # instantiate it to use it, although it absolutely can be used in ColliderComponents

    @staticmethod
    def get_aabb(transform: Transform) -> Rect:
        # Create the smallest possible rectangle for collision sake.
        rect = Rect(0, 0, 1, 1)
        rect.center = transform.position
        return rect

    @staticmethod
    def get_furthest_vertex(vector: Vector2, transform: Transform) -> Vector2:
        # A Point only has one point, so we always return that.
        # vector is only included to match signatures
        return transform.position

    @staticmethod
    def get_vertices() -> list[Vector2]:
        return (Vector2(0, 0),)

    def draw(
        self,
        edge_width: int = 1,
        edge_color: ColorLike = None,
        fill_color: ColorLike = None,
    ) -> Surface:
        surface = super().draw(edge_width, edge_color, fill_color)
        surface.fill(edge_color)
        return surface
