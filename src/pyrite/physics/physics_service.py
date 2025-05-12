from __future__ import annotations

from typing import TypeAlias, TYPE_CHECKING

import cffi
import pymunk

if TYPE_CHECKING:
    from pymunk import PointQueryInfo, SegmentQueryInfo, ShapeFilter


Point: TypeAlias = tuple[float, float]

# Calculating the system's max int value for setting the collision type of
# ColliderComponents
COMPONENT_TYPE: int = 2 ** (cffi.FFI().sizeof("int") * 8 - 1) - 1


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

    @classmethod
    def step(cls, delta_time: float):
        cls.space.step(delta_time)
