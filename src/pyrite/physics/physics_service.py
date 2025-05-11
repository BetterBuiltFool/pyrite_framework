from __future__ import annotations

from typing import TypeAlias, TYPE_CHECKING

import pymunk

if TYPE_CHECKING:
    from pymunk import PointQueryInfo, SegmentQueryInfo, ShapeFilter


Point: TypeAlias = tuple[float, float]


class PhysicsService:
    space = pymunk.Space()

    @staticmethod
    def cast_ray(
        start: Point, end: Point, shape_filter: ShapeFilter
    ) -> list[SegmentQueryInfo]:
        pass

    @staticmethod
    def cast_ray_single(
        start: Point, end: Point, shape_filter: ShapeFilter
    ) -> SegmentQueryInfo:
        pass

    @staticmethod
    def check_point(point: Point, shape_filer: ShapeFilter) -> PointQueryInfo:
        pass
