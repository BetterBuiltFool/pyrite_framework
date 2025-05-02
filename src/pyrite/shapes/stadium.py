from __future__ import annotations

import math
from typing import TYPE_CHECKING

from pygame import draw, Rect, Surface, Vector2

from ..transform import Transform
from ..types.shape import Shape


_vertical_axis = Vector2(0, 1)

if TYPE_CHECKING:
    from pygame.typing import ColorLike


class Stadium(Shape):
    """
    The 2D equivalent of a capsule.
    Defined by the radius of the semicircles and the height of the straight sides.

    Vertices: One for each focus, plus each end of the straight sides.
    """

    def __init__(self, radius: float, height: float) -> None:
        """
        The 2D equivalent of a capsule.

        Total height will be _height_ + 2 * _radius_

        Total width will be 2 * _radius_.

        :param radius: The radius of the semicircular ends.
        :param height: The height of the straight sides.
        """
        self.radius = radius
        self.height = height

    def get_furthest_vertex(self, vector: Vector2, transform: Transform) -> Vector2:
        # Rotate and scale vector by transform data
        # normalize vector
        vector = self._prescale_vector(vector, transform)
        # Offset to the closer of the two foci
        focus = vector * _vertical_axis
        y_offset = math.copysign(self.height / 2, focus)
        # Now we can treat it like a circle again.
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

    def draw(
        self,
        edge_width: int = 1,
        edge_color: ColorLike = None,
        fill_color: ColorLike = None,
    ) -> Surface:
        surface = super().draw(edge_width, edge_color, fill_color)
        origin = (surface.width / 2, surface.height / 2)
        if fill_color:
            draw.circle(surface, fill_color, origin + (0, self.height / 2), self.radius)
            draw.circle(surface, fill_color, origin - (0, self.height / 2), self.radius)
            center_rect = Rect(0, 0, surface.width, self.height)
            center_rect.center = origin
            draw.rect(surface, fill_color, center_rect)
        if edge_width > 0:

            top_rect = (
                0,
                0,
                surface.width,
                self.radius * 2,
            )
            draw.arc(surface, edge_color, top_rect, 0, math.pi, edge_width)

            bottom_rect = (
                0,
                surface.height - self.radius * 2,
                surface.width,
                self.radius * 2,
            )
            draw.arc(surface, edge_color, bottom_rect, math.pi, 0, edge_width)

            draw.line(
                surface,
                edge_color,
                (0, self.radius),
                (0, surface.height - self.radius),
                edge_width,
            )
            draw.line(
                surface,
                edge_color,
                (surface.width - edge_width, self.radius),
                (surface.width - edge_width, surface.height - self.radius),
                edge_width,
            )
            return surface

        return super().draw(edge_width, edge_color, fill_color)
