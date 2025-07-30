from __future__ import annotations

from typing import TYPE_CHECKING

from .physics_service import PhysicsService, PymunkPhysicsService
from ...types.service import ServiceProvider

if TYPE_CHECKING:
    # from pygame.typing import Point
    # from pymunk import (
    #     PointQueryInfo,
    #     SegmentQueryInfo,
    #     ShapeFilter,
    # )
    from ...physics.collider_component import ColliderComponent
    from ...physics.rigidbody_component import RigidbodyComponent


class PhysicsServiceProvider(ServiceProvider[PhysicsService]):
    _service: PhysicsService = PymunkPhysicsService()

    @classmethod
    def hotswap(cls, service: PhysicsService):
        cls._service.transfer(service)
        cls._service = service

    # -----------------------Delegates-----------------------
    @classmethod
    def add_rigidbody(cls, rigidbody: RigidbodyComponent):
        cls._service.add_rigidbody(rigidbody)

    @classmethod
    def add_collider(cls, collider: ColliderComponent):
        cls._service.add_collider(collider)

    # @classmethod
    # def cast_ray(
    #     cls, start: Point, end: Point, shape_filter: ShapeFilter
    # ) -> list[SegmentQueryInfo]:
    #     """
    #     Cast a ray from start to end, returning all collisions within.
    #     Due to the nature of the physics engine, rays cannot be infinite so an end
    #     point must be specifiied.

    #     :param start: A start point, in world space.
    #     :param end: An end point, in world space.
    #     :param shape_filter: A filter object used to filter out undesired shapes for
    #     collision.
    #     :return: A list of SegmentQueryInfos, one for each shape collided with.
    #     """
    #     cls._service.cast_ray(start, end, shape_filter)

    # @classmethod
    # def cast_ray_single(
    #     cls, start: Point, end: Point, shape_filter: ShapeFilter
    # ) -> SegmentQueryInfo:
    #     """
    #     Cast a ray from start to end, returning the _first_ collision it finds.
    #     Due to the nature of the physics engine, rays cannot be infinite so an end
    #     point must be specifiied.

    #     :param start: A start point, in world space.
    #     :param end: An end point, in world space.
    #     :param shape_filter: A filter object used to filter out undesired shapes for
    #     collision.
    #     :return: A SegmentQueryInfo, denoting information about the collided shape.
    #     """
    #     cls._service.cast_ray_single(start, end, shape_filter)

    # @classmethod
    # def check_point(cls, point: Point, shape_filer: ShapeFilter) -> PointQueryInfo:
    #     """
    #     Determines if a point in world space is within a shape.

    #     :param point: A point in world space.
    #     :param shape_filer: A filter object used to filter out undesired shapes for
    #     collision.
    #     :return: A SegmentQueryInfo, denoting information about the collided shape.
    #     """
    #     cls._service.check_point(point, shape_filer)

    @classmethod
    def set_gravity(cls, gravity_x: float, gravity_y: float):
        """
        Sets the gravity in the physics space.

        :param gravity_x: Pull force of gravity in the X direction
        :param gravity_y: Pull force of gravity in the Y direction
        """
        cls._service.set_gravity(gravity_x, gravity_y)

    @classmethod
    def step(cls, delta_time: float):
        """
        Steps the physics engine by the denoted amount.

        :param delta_time: The length of time to be simulated.
        """
        cls._service.step(delta_time)

    @classmethod
    def sync_bodies_to_transforms(cls):
        """
        Takes all TransformComponents with a rigidbody and updates the rigidbody to
        match the Transform if the transform has been set in the past frame.
        """
        cls._service.sync_bodies_to_transforms()

    @classmethod
    def sync_transforms_to_bodies(cls):
        """
        Takes all TransformComponents with a rigidbody and updates their position and
        rotation with the new calculations.
        """
        cls._service.sync_transforms_to_bodies()
