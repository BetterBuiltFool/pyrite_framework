from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from weakref import WeakKeyDictionary, WeakSet

from pygame import Vector2

from ...types.service import Service

if TYPE_CHECKING:
    from pygame.typing import Point
    from ...transform import Transform, TransformComponent


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
    def __init__(self) -> None:
        self.world_transforms: WeakKeyDictionary[TransformComponent, Transform] = (
            WeakKeyDictionary()
        )
        self.local_transforms: WeakKeyDictionary[TransformComponent, Transform] = (
            WeakKeyDictionary()
        )

        self.dirty_components: WeakSet[TransformComponent] = WeakSet()

    def transfer(self, target_service: TransformService):
        for component, transform in self.local_transforms.items():
            target_service.initialize_component(component, transform)

    def get_local(self, component: TransformComponent) -> Transform:
        return self.local_transforms.get(component)

    def get_local_position(self, component: TransformComponent) -> Point:
        return self.local_transforms.get(component).position

    def get_local_rotation(self, component: TransformComponent) -> float:
        return self.local_transforms.get(component).rotation

    def get_local_scale(self, component: TransformComponent) -> Point:
        return self.local_transforms.get(component).scale

    def set_local(self, component: TransformComponent, value: Transform):
        self.local_transforms.update({component: value})

    def set_local_position(self, component: TransformComponent, position: Point):
        self.dirty_components.add(component)
        self.local_transforms.get(component).position = Vector2(position)

    def set_local_rotation(self, component: TransformComponent, angle: Point):
        self.dirty_components.add(component)
        self.local_transforms.get(component).rotation = angle

    def set_local_scale(self, component: TransformComponent, scale: Point):
        self.dirty_components.add(component)
        self.local_transforms.get(component).scale = Vector2(scale)

    def get_world(self, component: TransformComponent) -> Transform:
        return self.world_transforms.get(component)

    def get_world_position(self, component: TransformComponent) -> Point:
        return self.world_transforms.get(component).position

    def get_world_rotation(self, component: TransformComponent) -> float:
        return self.world_transforms.get(component).rotation

    def get_world_scale(self, component: TransformComponent) -> Point:
        return self.world_transforms.get(component).scale

    def set_world(self, component: TransformComponent, value: Transform):
        # TODO Force update local
        self.world_transforms.update({component: value})

    def set_world_position(self, component: TransformComponent, position: Point):
        # TODO Force update local
        self.world_transforms.get(component).position = Vector2(position)

    def set_world_rotation(self, component: TransformComponent, angle: Point):
        # TODO Force update local
        self.world_transforms.get(component).rotation = angle

    def set_world_scale(self, component: TransformComponent, scale: Point):
        # TODO Force update local
        self.world_transforms.get(component).scale = Vector2(scale)

    def is_dirty(self, component: TransformComponent) -> bool:
        return component in self.dirty_components

    def clean(self, component: TransformComponent):
        self.dirty_components.discard(component)

    def get_dirty(self) -> set[TransformComponent]:
        return set(self.dirty_components)

    def initialize_component(self, component: TransformComponent, value: Transform):
        self.dirty_components.add(component)
        self.local_transforms.update({component: value})
        # Temporary, will update w/ TransformComponent updates
        self.world_transforms.update({component: value.copy()})
