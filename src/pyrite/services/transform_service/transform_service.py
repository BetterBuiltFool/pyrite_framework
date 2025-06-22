from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

# from pygame import Vector2

from ...transform import Transform
from ...types.service import Service

if TYPE_CHECKING:
    from pygame.typing import Point
    from ...transform.transform_component import TransformComponent


class TransformService(Service):

    @abstractmethod
    def get_local(self, component: TransformComponent) -> Transform:
        pass

    @abstractmethod
    def get_local_position(self, component: TransformComponent) -> Point:
        pass

    @abstractmethod
    def get_local_rotation(self, component: TransformComponent) -> float:
        pass

    @abstractmethod
    def get_local_scale(self, component: TransformComponent) -> Point:
        pass

    @abstractmethod
    def set_local(self, component: TransformComponent, value: Transform):
        pass

    @abstractmethod
    def set_local_position(self, component: TransformComponent, position: Point):
        pass

    @abstractmethod
    def set_local_rotation(self, component: TransformComponent, angle: Point):
        pass

    @abstractmethod
    def set_local_scale(self, component: TransformComponent, scale: Point):
        pass

    @abstractmethod
    def get_world(self, component: TransformComponent) -> Transform:
        pass

    @abstractmethod
    def get_world_position(self, component: TransformComponent) -> Point:
        pass

    @abstractmethod
    def get_world_rotation(self, component: TransformComponent) -> float:
        pass

    @abstractmethod
    def get_world_scale(self, component: TransformComponent) -> Point:
        pass

    @abstractmethod
    def set_world(self, component: TransformComponent, value: Transform):
        pass

    @abstractmethod
    def set_world_position(self, component: TransformComponent, position: Point):
        pass

    @abstractmethod
    def set_world_rotation(self, component: TransformComponent, angle: Point):
        pass

    @abstractmethod
    def set_world_scale(self, component: TransformComponent, scale: Point):
        pass

    @abstractmethod
    def is_dirty(self, component: TransformComponent) -> bool:
        pass

    @abstractmethod
    def clean(self, component: TransformComponent):
        pass

    @abstractmethod
    def get_dirty(
        self,
    ) -> set[TransformComponent]:
        pass

    @abstractmethod
    def initialize_component(self, component: TransformComponent, value: Transform):
        pass


class DefaultTransformService(TransformService):
    pass
