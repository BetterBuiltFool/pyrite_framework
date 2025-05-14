from __future__ import annotations

from typing import Any, TypeAlias, TYPE_CHECKING

import cffi

import pymunk

from .. import physics  # COMPONENT_TYPE, get_collider_components

if TYPE_CHECKING:
    from pymunk import (
        Arbiter,
        PointQueryInfo,
        SegmentQueryInfo,
        ShapeFilter,
        Space,
    )


Point: TypeAlias = tuple[float, float]

# Calculating the system's max int value for setting the collision type of
# ColliderComponents
# Recalculated here to avoid circular import
# TODO figure out an architecture that avoids this
COMPONENT_TYPE: int = 2 ** (cffi.FFI().sizeof("int") * 8 - 1) - 1


# Figure out where to put this so it doesn't cause circular imports
# Track _bodies here? Would remove RigidbodyComponent import
def post_solve(arbiter: Arbiter, space: Space, data: Any):
    collider1, collider2 = physics.get_collider_components(arbiter)
    if arbiter.is_first_contact:
        if collider1.compare_mask(collider2):
            collider1.OnTouch(collider1, collider2)
        if collider2.compare_mask(collider1):
            collider2.OnTouch(collider2, collider1)
    if collider1.compare_mask(collider2):
        collider1.WhileTouching(collider1, collider2)
    if collider2.compare_mask(collider1):
        collider2.WhileTouching(collider2, collider1)


class PhysicsService:
    space = pymunk.Space()
    comp_handler = space.add_collision_handler(COMPONENT_TYPE, COMPONENT_TYPE)
    comp_handler.post_solve = post_solve

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
