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
    """
    A service that provides data and convenience methods for physics operations.
    Acts as an abstraction over the underlying physics engine.

    Currently built around pymunk.

    TODO: Pull up more methods from the physics engine to reduce coupling.
    """

    space = pymunk.Space()
    comp_handler = space.add_collision_handler(COMPONENT_TYPE, COMPONENT_TYPE)
    bodies: WeakValueDictionary[Body, Any] = WeakValueDictionary()

    @staticmethod
    def cast_ray(
        start: Point, end: Point, shape_filter: ShapeFilter
    ) -> list[SegmentQueryInfo]:
        """
        Cast a ray from start to end, returning all collisions within.
        Due to the nature of the physics engine, rays cannot be infinite so an end
        point must be specifiied.

        :param start: A start point, in world space.
        :param end: An end point, in world space.
        :param shape_filter: A filter object used to filter out undesired shapes for
        collision.
        :return: A list of SegmentQueryInfos, one for each shape collided with.
        """
        pass

    @staticmethod
    def cast_ray_single(
        start: Point, end: Point, shape_filter: ShapeFilter
    ) -> SegmentQueryInfo:
        """
        Cast a ray from start to end, returning the _first_ collision it finds.
        Due to the nature of the physics engine, rays cannot be infinite so an end
        point must be specifiied.

        :param start: A start point, in world space.
        :param end: An end point, in world space.
        :param shape_filter: A filter object used to filter out undesired shapes for
        collision.
        :return: A SegmentQueryInfo, denoting information about the collided shape.
        """
        pass

    @staticmethod
    def check_point(point: Point, shape_filer: ShapeFilter) -> PointQueryInfo:
        """
        Determines if a point in world space is within a shape.

        :param point: A point in world space.
        :param shape_filer: A filter object used to filter out undesired shapes for
        collision.
        :return: A SegmentQueryInfo, denoting information about the collided shape.
        """
        pass

    @classmethod
    def step(cls, delta_time: float):
        """
        Steps the physics engine by the denoted amount.

        :param delta_time: The length of time to be simulated.
        """
        cls.space.step(delta_time)

    @classmethod
    def get_owner_from_body(cls, body: Body) -> Any | None:
        """
        Finds an owning object for a given physics Body, if it exists.

        :param body: A physics Body, belonging to a RigidbodyComponent
        :return: The owning object of the RigidbodyComponent, if it exists.
        """
        return cls.bodies.get(body)
