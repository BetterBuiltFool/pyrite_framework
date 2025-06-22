from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

# from weakref import WeakKeyDictionary, WeakSet

# from pygame import Vector2

from ...transform import Transform
from ...types.service import Service

if TYPE_CHECKING:
    from pygame.typing import Point
    from ...transform.transform_component import TransformComponent


class TransformService(Service):

    @abstractmethod
    def get_local(component: TransformComponent) -> Transform:
        pass

    @abstractmethod
    def get_local_position(component: TransformComponent) -> Point:
        pass

    @abstractmethod
    def get_local_rotation(component: TransformComponent) -> float:
        pass

    @abstractmethod
    def get_local_scale(component: TransformComponent) -> Point:
        pass

    @abstractmethod
    def set_local(component: TransformComponent, value: Transform):
        pass

    @abstractmethod
    def set_local_position(component: TransformComponent, position: Point):
        pass

    @abstractmethod
    def set_local_rotation(component: TransformComponent, angle: Point):
        pass

    @abstractmethod
    def set_local_scale(component: TransformComponent, scale: Point):
        pass

    @abstractmethod
    def get_world(component: TransformComponent) -> Transform:
        pass

    @abstractmethod
    def get_world_position(component: TransformComponent) -> Point:
        pass

    @abstractmethod
    def get_world_rotation(component: TransformComponent) -> float:
        pass

    @abstractmethod
    def get_world_scale(component: TransformComponent) -> Point:
        pass

    @abstractmethod
    def set_world(component: TransformComponent, value: Transform):
        pass

    @abstractmethod
    def set_world_position(component: TransformComponent, position: Point):
        pass

    @abstractmethod
    def set_world_rotation(component: TransformComponent, angle: Point):
        pass

    @abstractmethod
    def set_world_scale(component: TransformComponent, scale: Point):
        pass

    @abstractmethod
    def is_dirty(component: TransformComponent) -> bool:
        pass

    @abstractmethod
    def clean(component: TransformComponent):
        pass

    @abstractmethod
    def get_dirty() -> set[TransformComponent]:
        pass

    @abstractmethod
    def initialize_component(component: TransformComponent, value: Transform):
        pass


class DefaultTransformService(TransformService):
    pass
