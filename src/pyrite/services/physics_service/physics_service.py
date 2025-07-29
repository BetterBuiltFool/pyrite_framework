from __future__ import annotations

from abc import abstractmethod
import math
from typing import Any, TYPE_CHECKING
from weakref import WeakValueDictionary

import pymunk

from ...types.service import Service
from ...constants import COMPONENT_TYPE

if TYPE_CHECKING:
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


class PhysicsService(Service):

    @abstractmethod
    def add_rigidbody(self, rigidbody: RigidbodyComponent):
        pass

    @abstractmethod
    def add_collider(self, collider: ColliderComponent):
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
    def set_gravity(self, gravity_x: float, gravity_y: float):
        pass

    @abstractmethod
    def step(self, delta_time: float):
        pass

    @abstractmethod
    def sync_transforms_to_bodies(self):
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
        self.comp_handler.post_solve = PymunkPhysicsService.post_solve
        self.comp_handler.separate = PymunkPhysicsService.separate

    def transfer(self, target_service: PhysicsService):
        # Gotta figure out what to do here. I don't have any plans for other physics
        # engines, so I've not bothered with making things terribly abstract, meaning
        # that it's decidedly nontrivial to transfer physics data.
        pass

    def add_rigidbody(self, rigidbody: RigidbodyComponent):
        self.bodies[rigidbody.body] = rigidbody
        self.space.add(rigidbody.body)

    def add_collider(self, collider: ColliderComponent):
        self.space.add(*collider.shapes)

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

    def sync_transforms_to_bodies(self):
        # Passing TransformComponent class explicitly since we can't import it without
        # causing a cycle
        for body, rigidbody in self.bodies.items():
            transform = rigidbody.transform
            if body.is_sleeping or body.body_type == pymunk.Body.STATIC:
                # No adjustments to sleeping, static, or transformless objects
                continue
            # TODO calculate an expected interpolation value?
            new_pos = transform.world_position.lerp(body.position, 0.5)
            angle_between = (
                (math.degrees(body.angle) - transform.world_rotation) + 180
            ) % 360 - 180
            new_rot = angle_between / 2

            transform.world_position = new_pos
            transform.world_rotation = new_rot

    def post_solve(self, arbiter: Arbiter, space: Space, data: Any):
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

    def separate(self, arbiter: Arbiter, space: Space, data: Any):
        collider1, collider2 = self.get_collider_components(arbiter)
        if collider1.compare_mask(collider2):
            collider1.OnSeparate(collider1, collider2)
        if collider2.compare_mask(collider1):
            collider2.OnSeparate(collider2, collider1)

    def get_collider_components(
        self,
        arbiter: Arbiter,
    ) -> tuple[ColliderComponent, ColliderComponent]:
        shape1, shape2 = arbiter.shapes
        body1 = shape1.body
        body2 = shape2.body
        rigidbody_1 = self.bodies[body1]
        rigidbody_2 = self.bodies[body2]
        assert rigidbody_1.collider
        assert rigidbody_2.collider
        return rigidbody_1.collider, rigidbody_2.collider
