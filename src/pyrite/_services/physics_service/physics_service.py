from __future__ import annotations

from abc import abstractmethod
from collections.abc import Sequence
import math
from typing import Any, TYPE_CHECKING
from weakref import WeakValueDictionary

import pymunk
import pygame

from pyrite._types.service import Service
from pyrite.constants import COMPONENT_TYPE
from pyrite._physics.queries import PointInfo, SegmentInfo
from pyrite._physics.filter import Filter
from pyrite.utils import point_to_tuple
from pyrite._types.shape import Shape

if TYPE_CHECKING:
    from collections.abc import Iterator

    from pygame.typing import Point, RectLike
    from pymunk import (
        Arbiter,
        Body,
        Space,
    )
    from pyrite._component.collider_component import ColliderComponent
    from pyrite._component.rigidbody_component import RigidbodyComponent
    from pyrite._transform.transform import Transform
    from pyrite._types.constraint import Constraint


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

    @abstractmethod
    def add_collider_shapes(
        self,
        collider: ColliderComponent,
        shapes: Shape[pymunk.Shape] | Sequence[Shape[pymunk.Shape]],
    ) -> None:
        pass

    @abstractmethod
    def cast_ray(
        self, start: Point, end: Point, radius: float, shape_filter: Filter
    ) -> list[SegmentInfo]:
        pass

    @abstractmethod
    def cast_ray_single(
        self, start: Point, end: Point, radius: float, shape_filter: Filter
    ) -> SegmentInfo | None:
        pass

    @abstractmethod
    def check_area(self, area: RectLike, shape_filter: Filter) -> list[Shape]:
        pass

    @abstractmethod
    def check_point(
        self, point: Point, max_distance: float, shape_filter: Filter
    ) -> list[PointInfo]:
        pass

    @abstractmethod
    def check_point_nearest(
        self, point: Point, max_distance: float, shape_filter: Filter
    ) -> PointInfo | None:
        pass

    @abstractmethod
    def _force_sync_to_transform(self, rigidbody: RigidbodyComponent) -> None:
        pass

    @abstractmethod
    def clear_collider_shapes(self, collider: ColliderComponent) -> set[Shape]:
        pass

    @abstractmethod
    def remove_collider_shape(self, collider: ColliderComponent, shape: Shape) -> None:
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

            # Remove the bodies and constraints from the old space.
            self.space.remove(body.body)
            for constraint in body.constraints:
                self.space.remove(constraint._constraint)

            target_service.add_rigidbody(body)
            for constraint in body.constraints:
                target_service.add_constraint(constraint)
        for body in self.colliders.values():

            # Remove all shapes from the space
            collider = ColliderComponent.get(body.owner)
            assert collider
            for shape in collider.shapes:
                self.space.remove(shape._shape)

            target_service.add_collider(body)
            target_service.add_collider_shapes(collider, list(collider.shapes.keys()))

    def add_rigidbody(self, rigidbody: RigidbodyComponent):
        self.bodies[rigidbody.body] = rigidbody
        self.space.add(rigidbody.body)

    def add_collider(self, collider: ColliderComponent):
        self.colliders[collider.body] = collider

    def add_constraint(self, constraint: Constraint) -> None:
        self.space.add(constraint._constraint)

    def add_collider_shapes(
        self,
        collider: ColliderComponent,
        shapes: Shape[pymunk.Shape] | Sequence[Shape[pymunk.Shape]],
    ) -> None:
        if not isinstance(shapes, Sequence):
            shapes = [shapes]
        for shape in shapes:
            collider.shapes[shape] = None

            if shape.collider:
                self.remove_collider_shape(shape.collider, shape)
            shape.collider = collider

            shape._shape.collision_type = COMPONENT_TYPE
            shape._shape.body = collider.body
            shape._shape.filter = collider.filter
            if not (shape.density) and not (shape.mass or collider.body.mass):
                shape.density = 1

            self.space.add(shape._shape)

    def cast_ray(
        self, start: Point, end: Point, radius: float, shape_filter: Filter
    ) -> list[SegmentInfo]:
        queries = self.space.segment_query(
            point_to_tuple(start), point_to_tuple(end), radius, shape_filter._filter
        )

        return [SegmentInfo.from_query(query) for query in queries]

    def cast_ray_single(
        self, start: Point, end: Point, radius: float, shape_filter: Filter
    ) -> SegmentInfo | None:
        query = self.space.segment_query_first(
            point_to_tuple(start), point_to_tuple(end), radius, shape_filter._filter
        )
        if not query:
            return None

        return SegmentInfo.from_query(query)

    def check_area(self, area: RectLike, shape_filter: Filter) -> list[Shape]:
        rect = pygame.Rect(area)
        queries = self.space.bb_query(
            pymunk.BB(rect.left, rect.bottom, rect.right, rect.top),
            shape_filter._filter,
        )

        return [Shape._shapes[query_shape] for query_shape in queries]

    def check_point_nearest(
        self, point: Point, max_distance: float, shape_filter: Filter
    ) -> PointInfo | None:
        query = self.space.point_query_nearest(
            point_to_tuple(point), max_distance, shape_filter._filter
        )
        if not query:
            return None

        return PointInfo.from_query(query)

    def check_point(
        self, point: Point, max_distance: float, shape_filter: Filter
    ) -> list[PointInfo]:
        queries = self.space.point_query(
            point_to_tuple(point), max_distance, shape_filter._filter
        )

        return [PointInfo.from_query(query) for query in queries]

    def clear_collider_shapes(self, collider: ColliderComponent) -> set[Shape]:
        shapes = set(collider.shapes.keys())
        for shape in shapes:
            self.remove_collider_shape(collider, shape)
        return shapes

    def remove_collider_shape(
        self, collider: ColliderComponent, shape: Shape[pymunk.Shape]
    ) -> None:
        if shape in collider.shapes:
            collider.shapes.pop(shape)
        self.space.remove(shape._shape)
        shape._shape.body = None
        shape.collider = None

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
        body.angle = math.radians(transform.rotation)
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
                ((math.degrees(body.angle) - world_transform.rotation) + 180) % 360
            ) - 180
            new_rot = world_transform.rotation + (angle_between / 2)

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
