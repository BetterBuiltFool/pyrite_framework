from __future__ import annotations

from typing import TYPE_CHECKING

from pygame import Vector2
from pyrite._types.shape import Shape

if TYPE_CHECKING:
    from pymunk import PointQueryInfo, SegmentQueryInfo
    from pygame.typing import Point


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

    @staticmethod
    def from_query(query: PointQueryInfo) -> PointInfo:
        shape = None
        if query.shape:
            shape = Shape._shapes[query.shape]

        return PointInfo(shape, query.point, query.distance, query.gradient)


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

    @staticmethod
    def from_query(query: SegmentQueryInfo) -> SegmentInfo:
        shape = None
        if query.shape:
            shape = Shape._shapes[query.shape]

        return SegmentInfo(shape, query.point, query.normal, query.alpha)
