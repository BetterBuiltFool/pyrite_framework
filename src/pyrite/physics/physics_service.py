from __future__ import annotations

from typing import Any, TypeAlias, TYPE_CHECKING
from weakref import WeakValueDictionary

import cffi
import pymunk

# from .. import physics  # COMPONENT_TYPE, get_collider_components

if TYPE_CHECKING:
    from pymunk import (
        Body,
        PointQueryInfo,
        SegmentQueryInfo,
        ShapeFilter,
    )


Point: TypeAlias = tuple[float, float]

# Calculating the system's max int value for setting the collision type of
# ColliderComponents
# Recalculated here to avoid circular import
# TODO figure out an architecture that avoids this
COMPONENT_TYPE: int = 2 ** (cffi.FFI().sizeof("int") * 8 - 1) - 1


class PhysicsService:
    space = pymunk.Space()
    comp_handler = space.add_collision_handler(COMPONENT_TYPE, COMPONENT_TYPE)
    bodies: WeakValueDictionary[Body, Any] = WeakValueDictionary()

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

    @classmethod
    def get_owner_from_body(cls, body: Body) -> Any | None:
        return cls.bodies.get(body)
