from __future__ import annotations

from abc import abstractmethod

from ..types import System
from .transform import Transform
from . import transform_service


class TransformSystem(System):

    @abstractmethod
    def to_world(self, transform: Transform, context: Transform) -> Transform:
        pass

    @abstractmethod
    def to_local(self, transform: Transform, context: Transform) -> Transform:
        pass


class DefaultTransformSystem(TransformSystem):

    def to_world(self, transform: Transform, context: Transform) -> Transform:
        return transform

    def to_local(self, transform: Transform, context: Transform) -> Transform:
        return transform

    def pre_render(self, delta_time: float) -> None:
        for component in transform_service.get_dirty():
            transform = transform_service.get_local(component)
            transform_service.set_world(component, transform)
            transform_service.clean(component)
