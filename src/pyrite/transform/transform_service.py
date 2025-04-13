from __future__ import annotations

from typing import TYPE_CHECKING
from weakref import WeakKeyDictionary, WeakSet

from .transform import Transform

if TYPE_CHECKING:
    from .transform_component import TransformComponent


local_transforms: WeakKeyDictionary[TransformComponent, Transform] = WeakKeyDictionary()
world_transforms: WeakKeyDictionary[TransformComponent, Transform] = WeakKeyDictionary()

dirty_components: WeakSet[TransformComponent] = WeakSet()


def get_local(component: TransformComponent) -> Transform:
    return local_transforms.get(component)


def set_local(component: TransformComponent, value: Transform):
    dirty_components.add(component)
    local_transforms.update({component: value})


def get_world(component: TransformComponent) -> Transform:
    return local_transforms.get(component)


def set_world(component: TransformComponent, value: Transform):
    world_transforms.update({component: value})


def is_dirty(component: TransformComponent) -> bool:
    return component in dirty_components


def initialize_component(component: TransformComponent, value: Transform):
    local_transforms.update({component: value})
    world_transforms.update({component: value})  # Defaulting, will update
