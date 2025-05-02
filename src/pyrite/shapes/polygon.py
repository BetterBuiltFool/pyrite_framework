from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING
from pygame import Surface, Vector2

from ..types.shape import Shape

if TYPE_CHECKING:
    from ..transform import Transform
    from pygame.typing import ColorLike


def _get_furthest(direction: Vector2, point_a: Vector2, point_b: Vector2) -> Vector2:
    a = point_a * direction
    b = point_b * direction
    return point_a if a > b else point_b


class Polygon(Shape):
    """
    A shape made from arbitray vertices.
    Must be convex to draw or collide properly.

    :Vertices: Custom.
    """

    def __init__(self, vertices: Sequence[Vector2]) -> None:
        """
        A shape made from arbitray vertices.
        Must be convex to draw or collide properly.

        If the vertices are not in order, the collsion algorithm will operate on the
        convex hull of the shape.

        :param vertices: A sequence of points representing the vertices of the polygon.
        """
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

    def get_vertices(self) -> tuple[Vector2]:
        return tuple(self._vertices)

    def draw(
        self,
        edge_width: int = 1,
        edge_color: ColorLike = None,
        fill_color: ColorLike = None,
    ) -> Surface:
        surface = super().draw(edge_width, edge_color, fill_color)
        # TODO Implement this!
        raise NotImplementedError("Cannot draw polygons yet.")
        if fill_color is not None:
            # Draw the filled polygon by forming triangles from edges to origin
            pass
        if edge_width > 0:
            # Loop the vertices, and draw the lines along the edges
            pass

        return surface
