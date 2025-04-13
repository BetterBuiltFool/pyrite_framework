from __future__ import annotations

from typing import TYPE_CHECKING
from weakref import WeakKeyDictionary

from .transform import Transform

if TYPE_CHECKING:
    from .transform_component import TransformComponent


local_transforms: WeakKeyDictionary[TransformComponent, Transform] = WeakKeyDictionary()
world_transforms: WeakKeyDictionary[TransformComponent, Transform] = WeakKeyDictionary()


def get_local(component: TransformComponent) -> Transform:
    return local_transforms.get(component)


def set_local(component: TransformComponent, value: Transform):
    local_transforms.update({component: value})


def get_world(component: TransformComponent) -> Transform:
    return local_transforms.get(component)


def set_world(component: TransformComponent, value: Transform):
    world_transforms.update({component: value})


def initialize_component(component: TransformComponent, value: Transform):
    local_transforms.update({component: value})
    world_transforms.update({component: value})  # Defaulting, will update
