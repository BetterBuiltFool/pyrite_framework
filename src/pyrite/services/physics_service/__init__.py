from __future__ import annotations

from typing import TYPE_CHECKING

import pymunk

from .physics_service import PhysicsService, PymunkPhysicsService
from ...types.service import ServiceProvider

if TYPE_CHECKING:
    from collections.abc import Iterator, Sequence
    from ...physics.collider_component import ColliderComponent
    from ...physics.rigidbody_component import RigidbodyComponent
    from ...transform import Transform
    from ...types.constraint import Constraint
    from pyrite.types.shape import Shape


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

    @classmethod
    def add_constraint(cls, constraint: Constraint):
        cls._service.add_constraint(constraint)

    @classmethod
    def add_collider_shapes(
        cls,
        collider: ColliderComponent,
        shapes: Shape[pymunk.Shape] | Sequence[Shape[pymunk.Shape]],
    ) -> None:
        """
        Adds the shape or sequence of shapes to the provided ColliderComponent

        :param collider: a collider component receiving new shapes.
        :param shapes: A shape or sequence of shapes.
        """
        cls._service.add_collider_shapes(collider, shapes)

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
    def clear_collider_shapes(cls, collider: ColliderComponent) -> set[Shape]:
        """
        Removes all shapes from the given collider.

        :param collider: The collider whose shapes are being removed.
        :return: A set containing all previous shapes from the collider.
        """
        return cls._service.clear_collider_shapes(collider)

    @classmethod
    def remove_collider_shape(cls, collider: ColliderComponent, shape: Shape) -> None:
        """
        Removes a given shape from a collider.

        :param collider: The collider whose shape is being removed.
        :param shape: The shape to be removed from the collider. If the shape does not
            belong to the collider, nothing will happen.
        """
        cls._service.remove_collider_shape(collider, shape)

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
    def _force_sync_to_transform(cls, rigidbody: RigidbodyComponent) -> None:
        """
        Forces the RigidbodyComponent to sync up with its associated transform.
        """
        cls._service._force_sync_to_transform(rigidbody)

    @classmethod
    def sync_bodies_to_transforms(cls):
        """
        Takes all TransformComponents with a rigidbody and updates the rigidbody to
        match the Transform if the transform has been set in the past frame.
        """
        cls._service.sync_bodies_to_transforms()

    @classmethod
    def get_updated_transforms_for_bodies(
        cls,
    ) -> Iterator[tuple[RigidbodyComponent, Transform]]:
        """
        Provides an iterator containing Rigidbodies and their new transforms.
        """
        yield from cls._service.get_updated_transforms_for_bodies()
