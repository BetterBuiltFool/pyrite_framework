from __future__ import annotations

from typing import TYPE_CHECKING
from weakref import WeakKeyDictionary, WeakSet

from pygame import Vector2

from .transform import Transform

if TYPE_CHECKING:
    from .transform_component import TransformComponent
    from pygame.typing import Point


local_transforms: WeakKeyDictionary[TransformComponent, Transform] = WeakKeyDictionary()
world_transforms: WeakKeyDictionary[TransformComponent, Transform] = WeakKeyDictionary()

dirty_components: WeakSet[TransformComponent] = WeakSet()


def get_local(component: TransformComponent) -> Transform:
    """
    :param component: Any transform component.
    :return: The Transform object representing _component_ in local space.
    """
    return local_transforms.get(component)


def get_local_position(component: TransformComponent) -> Point:
    """
    :param component: Any transform component.
    :return: The current position of _component_, in local space.
    """
    return local_transforms.get(component).position


def get_local_rotation(component: TransformComponent) -> float:
    """
    :param component: Any transform component.
    :return: The current rotation of _component_, in local space.
    """
    return local_transforms.get(component).rotation


def get_local_scale(component: TransformComponent) -> Point:
    """
    :param component: Any transform component.
    :return: The current scaling factor of _component_, in local space.
    """
    return local_transforms.get(component).scale


def set_local(component: TransformComponent, value: Transform):
    """
    Forces the local transform value of a transform component to a new value.
    Does not mark the component for updates.

    :param component: Any transform component.
    :param value: A Transform value, in local space.
    """
    local_transforms.update({component: value})


def set_local_position(component: TransformComponent, position: Point):
    """
    Sets the position of the transform component to the new position.
    The component will be marked for updating.

    :param component: Any transform component.
    :param position: A point in local space.
    """
    dirty_components.add(component)
    local_transforms.get(component).position = Vector2(position)


def set_local_rotation(component: TransformComponent, angle: Point):
    """
    Sets the rotation of the transform component to the new rotation.
    The component will be marked for updating.

    :param component: Any transform component.
    :param angle: An angle in local space.
    """
    dirty_components.add(component)
    local_transforms.get(component).rotation = angle


def set_local_scale(component: TransformComponent, scale: Point):
    """
    Sets the scale of the transform component to the new scaling factor.
    The component will be marked for updating.

    :param component: Any transform component.
    :param position: A tuple with scaling factors for each dimension, in local space.
    """
    dirty_components.add(component)
    local_transforms.get(component).scale = Vector2(scale)


def get_world(component: TransformComponent) -> Transform:
    return world_transforms.get(component)


def get_world_position(component: TransformComponent) -> Point:
    return world_transforms.get(component).position


def get_world_rotation(component: TransformComponent) -> float:
    return world_transforms.get(component).rotation


def get_world_scale(component: TransformComponent) -> Point:
    return world_transforms.get(component).scale


def set_world(component: TransformComponent, value: Transform):
    world_transforms.update({component: value})


def set_world_position(component: TransformComponent, position: Point):
    # TODO Force update local values
    world_transforms.get(component).position = Vector2(position)


def set_world_rotation(component: TransformComponent, angle: Point):
    world_transforms.get(component).rotation = angle


def set_world_scale(component: TransformComponent, scale: Point):
    world_transforms.get(component).scale = Vector2(scale)


def is_dirty(component: TransformComponent) -> bool:
    return component in dirty_components


def clean(component: TransformComponent):
    dirty_components.discard(component)


def get_dirty() -> set[TransformComponent]:
    return set(dirty_components)


def initialize_component(component: TransformComponent, value: Transform):
    local_transforms.update({component: value})
    world_transforms.update({component: value.copy()})  # Defaulting, will update
