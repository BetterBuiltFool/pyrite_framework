from __future__ import annotations

from abc import abstractmethod

from ..types import System
from .transform import Transform
from . import transform_service


class TransformSystem(System):

    @staticmethod
    def to_world(transform: Transform, context: Transform) -> Transform:
        pass

    @staticmethod
    def to_local(transform: Transform, context: Transform) -> Transform:
        pass

    @staticmethod
    @abstractmethod
    def convert_to_world(transform: Transform) -> Transform:
        pass

    @staticmethod
    @abstractmethod
    def convert_to_local(transform: Transform) -> Transform:
        pass


class DefaultTransformSystem(TransformSystem):

    @staticmethod
    def convert_to_world(transform: Transform) -> Transform:
        return transform

    @staticmethod
    def convert_to_local(transform: Transform) -> Transform:
        return transform

    def pre_render(self, delta_time: float) -> None:
        for component in transform_service.get_dirty():
            transform = transform_service.get_local(component)
            transform_service.set_world(component, transform)
            transform_service.clean(component)


_default_transform_system: type[TransformSystem] = DefaultTransformSystem


def get_default_transform_system_type() -> type[TransformSystem]:
    return _default_transform_system


def set_default_transform_system_type(system_type: type[TransformSystem]):
    global _default_transform_system
    _default_transform_system = system_type
