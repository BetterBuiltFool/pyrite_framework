from __future__ import annotations

from abc import abstractmethod
import math
from typing import Any, TYPE_CHECKING
from weakref import WeakValueDictionary

import pymunk

from ...types.service import Service
from ...constants import COMPONENT_TYPE

if TYPE_CHECKING:
    from collections.abc import Iterator

    # from pygame.typing import Point
    from pymunk import (
        Arbiter,
        Body,
        # PointQueryInfo,
        # SegmentQueryInfo,
        # ShapeFilter,
        Space,
    )
    from ...physics.collider_component import ColliderComponent
    from ...physics.rigidbody_component import RigidbodyComponent
    from ...transform import Transform
    from ...types.constraint import Constraint


class PhysicsService(Service):

    @abstractmethod
    def add_rigidbody(self, rigidbody: RigidbodyComponent):
        pass

    @abstractmethod
    def add_collider(self, collider: ColliderComponent):
        pass

    @abstractmethod
    def add_constraint(self, constraint: Constraint) -> None:
        pass

        # @abstractmethod
        # def cast_ray(
        #     self, start: Point, end: Point, shape_filter: ShapeFilter
        # ) -> list[SegmentQueryInfo]:
        #     pass

        # @abstractmethod
        # def cast_ray_single(
        #     self, start: Point, end: Point, shape_filter: ShapeFilter
        # ) -> SegmentQueryInfo:
        #     pass

        # @abstractmethod
        # def check_point(
        #     self, point: Point, shape_filer: ShapeFilter
        # ) -> PointQueryInfo:
        # pass

    @abstractmethod
    def _force_sync_to_transform(self, rigidbody: RigidbodyComponent) -> None:
        pass

    @abstractmethod
    def set_gravity(self, gravity_x: float, gravity_y: float):
        pass

    @abstractmethod
    def step(self, delta_time: float):
        pass

    @abstractmethod
    def sync_bodies_to_transforms(self):
        pass

    @abstractmethod
    def get_updated_transforms_for_bodies(
        self,
    ) -> Iterator[tuple[RigidbodyComponent, Transform]]:
        pass


class PymunkPhysicsService(PhysicsService):

    def __init__(self) -> None:
        self.space = pymunk.Space()
        self.comp_handler = self.space.add_collision_handler(
            COMPONENT_TYPE, COMPONENT_TYPE
        )
        self.bodies: WeakValueDictionary[Body, RigidbodyComponent] = (
            WeakValueDictionary()
        )

        self.colliders: WeakValueDictionary[Body, ColliderComponent] = (
            WeakValueDictionary()
        )

        def post_solve(arbiter: Arbiter, space: Space, data: Any):
            collider1, collider2 = self.get_collider_components(arbiter)
            if arbiter.is_first_contact:
                if collider1.compare_mask(collider2):
                    collider1.OnTouch(collider1, collider2)
                if collider2.compare_mask(collider1):
                    collider2.OnTouch(collider2, collider1)
            if collider1.compare_mask(collider2):
                collider1.WhileTouching(collider1, collider2)
            if collider2.compare_mask(collider1):
                collider2.WhileTouching(collider2, collider1)

        def separate(arbiter: Arbiter, space: Space, data: Any):
            collider1, collider2 = self.get_collider_components(arbiter)
            if collider1.compare_mask(collider2):
                collider1.OnSeparate(collider1, collider2)
            if collider2.compare_mask(collider1):
                collider2.OnSeparate(collider2, collider1)

        self.comp_handler.post_solve = post_solve
        self.comp_handler.separate = separate

    def transfer(self, target_service: PhysicsService):
        for body in self.bodies.values():
            target_service.add_rigidbody(body)
        for body in self.colliders.values():
            target_service.add_collider(body)

    def add_rigidbody(self, rigidbody: RigidbodyComponent):
        self.bodies[rigidbody.body] = rigidbody
        self.space.add(rigidbody.body)

    def add_collider(self, collider: ColliderComponent):
        self.colliders[collider.body] = collider
        self.space.add(*[shape._shape for shape in collider.shapes])

    def add_constraint(self, constraint: Constraint) -> None:
        self.space.add(constraint._constraint)

    # def cast_ray(
    #     self, start: Point, end: Point, shape_filter: ShapeFilter
    # ) -> list[SegmentQueryInfo]:
    #     # TODO Implement this, just checking boxes right now
    #     pass

    # def cast_ray_single(
    #     self, start: Point, end: Point, shape_filter: ShapeFilter
    # ) -> SegmentQueryInfo:
    #     # TODO Implement this, just checking boxes right now
    #     pass

    # def check_point(self, point: Point, shape_filer: ShapeFilter) -> PointQueryInfo:
    #     # TODO Implement this, just checking boxes right now
    #     pass

    def set_gravity(self, gravity_x: float, gravity_y: float):
        self.space.gravity = (gravity_x, gravity_y)

    def step(self, delta_time: float):
        return self.space.step(delta_time)

    def sync_bodies_to_transforms(self):
        for rigidbody in self.bodies.values():
            transform = rigidbody.transform
            if not transform.has_changed():
                continue
            self._force_sync_to_transform(rigidbody)

    def _force_sync_to_transform(self, rigidbody: RigidbodyComponent) -> None:
        transform = rigidbody.transform
        body = rigidbody.body
        body.position = tuple(transform.position)
        body.angle = transform.rotation
        self.space.reindex_shapes_for_body(body)

    def get_updated_transforms_for_bodies(
        self,
    ) -> Iterator[tuple[RigidbodyComponent, Transform]]:
        for body, rigidbody in self.bodies.items():
            transform = rigidbody.transform
            if body.is_sleeping or body.body_type == pymunk.Body.STATIC:
                # No adjustments to sleeping, static, or transformless objects
                continue
            # TODO calculate an expected interpolation value?
            world_transform = transform.world()

            new_pos = world_transform.position.lerp(body.position, 0.5)
            angle_between = (
                (math.degrees(body.angle) - world_transform.rotation) + 180
            ) % 360 - 180
            new_rot = angle_between / 2

            new_transform = world_transform.copy()
            new_transform.position = new_pos
            new_transform.rotation = new_rot

            yield (rigidbody, new_transform)

    def get_collider_components(
        self,
        arbiter: Arbiter,
    ) -> tuple[ColliderComponent, ColliderComponent]:
        shape1, shape2 = arbiter.shapes
        body1 = shape1.body
        body2 = shape2.body
        collider1 = self.colliders[body1]
        collider2 = self.colliders[body2]
        return collider1, collider2
