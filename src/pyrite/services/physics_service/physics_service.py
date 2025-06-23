from __future__ import annotations

from abc import abstractmethod
from typing import Any, TYPE_CHECKING
from weakref import WeakValueDictionary

import pymunk

from ...types.service import Service
from ...constants import COMPONENT_TYPE

if TYPE_CHECKING:
    from pygame.typing import Point
    from pymunk import (
        Body,
        PointQueryInfo,
        SegmentQueryInfo,
        Shape,
        ShapeFilter,
    )


class PhysicsService(Service):

    @abstractmethod
    def add_collision_shape(self, collision_shape: Shape):
        pass

    @abstractmethod
    def cast_ray(
        self, start: Point, end: Point, shape_filter: ShapeFilter
    ) -> list[SegmentQueryInfo]:
        pass

    @abstractmethod
    def cast_ray_single(
        self, start: Point, end: Point, shape_filter: ShapeFilter
    ) -> SegmentQueryInfo:
        pass

    @abstractmethod
    def check_point(self, point: Point, shape_filer: ShapeFilter) -> PointQueryInfo:
        pass

    @abstractmethod
    def set_gravity(self, gravity: Point):
        pass

    @abstractmethod
    def step(self, delta_time: float):
        pass

    @abstractmethod
    def get_owner_from_body(self, body: Body) -> Any | None:
        pass


class PymunkPhysicsService(PhysicsService):

    def __init__(self) -> None:
        self.space = pymunk.Space()
        self.comp_handler = self.space.add_collision_handler(
            COMPONENT_TYPE, COMPONENT_TYPE
        )
        self.bodies: WeakValueDictionary[Body, Any] = WeakValueDictionary()

    def transfer(self, target_service: PhysicsService):
        # Gotta figure out what to do here. I don't have any plans for other physics
        # engines, so I've not bothered with making things terribly abstract, meaning
        # that it's decidedly nontrivial to transfer physics data.
        pass

    def add_collision_shape(self, collision_shape: Shape):
        self.space.add(collision_shape)

    def cast_ray(
        self, start: Point, end: Point, shape_filter: ShapeFilter
    ) -> list[SegmentQueryInfo]:
        # TODO Implement this, just checking boxes right now
        pass

    def cast_ray_single(
        self, start: Point, end: Point, shape_filter: ShapeFilter
    ) -> SegmentQueryInfo:
        # TODO Implement this, just checking boxes right now
        pass

    def check_point(self, point: Point, shape_filer: ShapeFilter) -> PointQueryInfo:
        # TODO Implement this, just checking boxes right now
        pass

    def set_gravity(self, gravity_pull: Point):
        self.space.gravity = gravity_pull

    def step(self, delta_time: float):
        return self.space.step(delta_time)

    def get_owner_from_body(self, body: Body) -> Any | None:
        return self.bodies.get(body)
