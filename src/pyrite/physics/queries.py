from __future__ import annotations

from typing import TYPE_CHECKING

from pygame import Vector2

if TYPE_CHECKING:
    from pygame.typing import Point

    from pyrite.types.shape import Shape


class PointInfo:
    """
    Contains information about a point query.
    """

    def __init__(
        self,
        shape: Shape | None,
        point: Point,
        distance: float,
        gradient: Point,
    ) -> None:
        self.shape = shape
        self.point = Vector2(point)
        self.distance = distance
        self.gradient = Vector2(gradient)


class SegmentInfo:
    """
    Contains information for a ray cast.
    """

    def __init__(
        self, shape: Shape | None, point: Point, normal: Point, alpha: float
    ) -> None:
        self.shape = shape
        self.point = Vector2(point)
        self.normal = Vector2(normal)
        self.alpha = alpha
