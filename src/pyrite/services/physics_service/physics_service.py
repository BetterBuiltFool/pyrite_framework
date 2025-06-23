from __future__ import annotations

from abc import abstractmethod
from typing import Any, TYPE_CHECKING

from ...types.service import Service

if TYPE_CHECKING:
    from pygame.typing import Point
    from pymunk import (
        Body,
        PointQueryInfo,
        SegmentQueryInfo,
        ShapeFilter,
    )


class PhysicsService(Service):

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
    def step(self, delta_time: float):
        pass

    @abstractmethod
    def get_owner_from_body(self, body: Body) -> Any | None:
        pass


class PymunkPhysicsService(PhysicsService):
    pass
