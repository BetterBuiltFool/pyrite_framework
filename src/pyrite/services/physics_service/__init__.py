from __future__ import annotations

from typing import Any, TYPE_CHECKING

from .physics_service import PhysicsService, PymunkPhysicsService
from ...types.service import ServiceProvider

if TYPE_CHECKING:
    from pygame.typing import Point
    from pymunk import (
        Body,
        PointQueryInfo,
        SegmentQueryInfo,
        ShapeFilter,
    )


class PhysicsServiceProvider(ServiceProvider):
    _service: PhysicsService = PymunkPhysicsService()

    @classmethod
    def hotswap(cls, service: PhysicsService):
        cls._service.transfer(service)
        cls._service = service

    # -----------------------Delegates-----------------------

    @classmethod
    def cast_ray(
        cls, start: Point, end: Point, shape_filter: ShapeFilter
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
        cls._service.cast_ray(start, end, shape_filter)

    @classmethod
    def cast_ray_single(
        cls, start: Point, end: Point, shape_filter: ShapeFilter
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
        cls._service.cast_ray_single(start, end, shape_filter)

    @classmethod
    def check_point(cls, point: Point, shape_filer: ShapeFilter) -> PointQueryInfo:
        """
        Determines if a point in world space is within a shape.

        :param point: A point in world space.
        :param shape_filer: A filter object used to filter out undesired shapes for
        collision.
        :return: A SegmentQueryInfo, denoting information about the collided shape.
        """
        cls._service.check_point(point, shape_filer)

    @classmethod
    def set_gravity(cls, gravity_pull: Point):
        """
        Sets the gravity in the physics space.

        :param gravity: A tuple of floats describing the direction of gravity's pull.
        """
        cls._service.set_gravity(gravity_pull)

    @classmethod
    def step(cls, delta_time: float):
        """
        Steps the physics engine by the denoted amount.

        :param delta_time: The length of time to be simulated.
        """
        cls._service.step(delta_time)

    @classmethod
    def get_owner_from_body(cls, body: Body) -> Any | None:
        """
        Finds an owning object for a given physics Body, if it exists.

        :param body: A physics Body, belonging to a RigidbodyComponent
        :return: The owning object of the RigidbodyComponent, if it exists.
        """
        cls._service.get_owner_from_body(body)
