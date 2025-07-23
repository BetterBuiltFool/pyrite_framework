from __future__ import annotations

from typing import TYPE_CHECKING

from ...types.service import ServiceProvider
from .transform_service import (
    TransformService,
    DefaultTransformService,
)

if TYPE_CHECKING:
    from collections.abc import Iterator
    from pygame.typing import Point
    from pygame import Vector2
    from ...transform import Transform, TransformComponent


class TransformServiceProvider(ServiceProvider[TransformService]):
    """
    Service that contains and maintains data for TransformComponents
    """

    _service: TransformService = DefaultTransformService()

    @classmethod
    def hotswap(cls, service: TransformService):
        cls._service.transfer(service)
        cls._service = service

    # -----------------------Delegates-----------------------

    @classmethod
    def get_local(cls, component: TransformComponent) -> Transform:
        """
        :param component: Any transform component.
        :return: The Transform object representing _component_ in local space.
        """
        return cls._service.get_local(component)

    @classmethod
    def get_local_position(cls, component: TransformComponent) -> Vector2:
        """
        :param component: Any transform component.
        :return: The current position of _component_, in local space.
        """
        return cls._service.get_local_position(component)

    @classmethod
    def get_local_rotation(cls, component: TransformComponent) -> float:
        """
        :param component: Any transform component.
        :return: The current rotation of _component_, in local space.
        """
        return cls._service.get_local_rotation(component)

    @classmethod
    def get_local_scale(cls, component: TransformComponent) -> Vector2:
        """
        :param component: Any transform component.
        :return: The current scaling factor of _component_, in local space.
        """
        return cls._service.get_local_scale(component)

    @classmethod
    def set_local(cls, component: TransformComponent, value: Transform):
        """
        Forces the local transform value of a transform component to a new value.
        Does not mark the component for updates.

        :param component: Any transform component.
        :param value: A Transform value, in local space.
        """
        return cls._service.set_local(component, value)

    @classmethod
    def set_local_position(cls, component: TransformComponent, position: Point):
        """
        Sets the position of the transform component to the new position.
        The component will be marked for updating.

        :param component: Any transform component.
        :param position: A point in local space.
        """
        return cls._service.set_local_position(component, position)

    @classmethod
    def set_local_rotation(cls, component: TransformComponent, angle: float):
        """
        Sets the rotation of the transform component to the new rotation.
        The component will be marked for updating.

        :param component: Any transform component.
        :param angle: An angle in local space.
        """
        return cls._service.set_local_rotation(component, angle)

    @classmethod
    def set_local_scale(cls, component: TransformComponent, scale: Point):
        """
        Sets the scale of the transform component to the new scaling factor.
        The component will be marked for updating.

        :param component: Any transform component.
        :param position: A tuple with scaling factors for each dimension, in local
            space.
        """
        return cls._service.set_local_scale(component, scale)

    @classmethod
    def get_world(cls, component: TransformComponent) -> Transform:
        """
        :param component: Any transform component.
        :return: A Transform object representing _component_ in world space.
        """
        return cls._service.get_world(component)

    @classmethod
    def get_world_position(cls, component: TransformComponent) -> Vector2:
        """
        :param component: Any transform component.
        :return: The current position of _component_, in world space.
        """
        return cls._service.get_world_position(component)

    @classmethod
    def get_world_rotation(cls, component: TransformComponent) -> float:
        """
        :param component: Any transform component.
        :return: The current rotation of _component_, in world space.
        """
        return cls._service.get_world_rotation(component)

    @classmethod
    def get_world_scale(cls, component: TransformComponent) -> Vector2:
        """
        :param component: Any transform component.
        :return: The current scaling factor of _component_, in world space.
        """
        return cls._service.get_world_scale(component)

    @classmethod
    def set_world(cls, component: TransformComponent, value: Transform):
        """
        Forces the world transform value of a transform component to a new value.
        The local transform will be updated to match.


        :param component: Any transform component.
        :param value: A Transform value, in world space.
        """
        return cls._service.set_world(component, value)

    @classmethod
    def _set_world_no_update(cls, component: TransformComponent, value: Transform):
        cls._service._set_world_no_update(component, value)

    @classmethod
    def set_world_position(cls, component: TransformComponent, position: Point):
        """
        Sets the position of the transform component to the new position.
        The component will be marked for updating.

        :param component: Any transform component.
        :param position: A point in world space.
        """
        return cls._service.set_world_position(component, position)

    @classmethod
    def set_world_rotation(cls, component: TransformComponent, angle: float):
        """
        Sets the rotation of the transform component to the new rotation.
        The component will be marked for updating.

        :param component: Any transform component.
        :param angle: An angle in world space.
        """
        return cls._service.set_world_rotation(component, angle)

    @classmethod
    def set_world_scale(cls, component: TransformComponent, scale: Point):
        """
        Sets the scale of the transform component to the new scaling factor.
        The component will be marked for updating.

        :param component: Any transform component.
        :param position: A tuple with scaling factors for each dimension, in world
            space.
        """
        return cls._service.set_world_scale(component, scale)

    @classmethod
    def get_parent(cls, component: TransformComponent) -> TransformComponent | None:
        """
        Finds the next higher transform component, if it exists.

        :param component: A TransformComponent somewhere in the hierarchy
        :return: The parent TransformComponent, if it exists, or None
        """
        return cls._service.get_parent(component)

    @classmethod
    def set_relative_to(
        cls, dependent: TransformComponent, relative: TransformComponent
    ) -> None:
        """
        Marks the given component as being relative to another. The parent component
        should not be a descendant of the child component.

        :param dependent: A TransformComponent
        :param relative: Another TransformComponent
        """
        return cls._service.set_relative_to(dependent, relative)

    @classmethod
    def get_descendants(cls, component: TransformComponent) -> set[TransformComponent]:
        """
        Provides a set of all immediate descendants of the given transform component.
        If it has no descendants, the set will be empty.

        :param component: A TransformComponent.
        :return: The immediately descending transform components of _component_.
        """
        return cls._service.get_descendants(component)

    @classmethod
    def traverse_transforms(cls) -> Iterator[TransformComponent | None]:
        """
        Provides an iterator walks down the tree of transform components, depth-first.

        :yield: The next TransformComponent in the tree, or None, if the
        TransformComponent has since expired.
        """
        yield from cls._service

    @classmethod
    def make_dirty(cls, component: TransformComponent) -> None:
        """
        Forces the component to be marked as dirty.

        :param component: A TransformComponent that will be marked as dirty.
        """
        cls._service.make_dirty(component)

    @classmethod
    def is_dirty(cls, component: TransformComponent) -> bool:
        """
        Checks if a transform component is in need of updating.

        :param component: Any transform component.
        :return: True if _component_ needs cleaning, False otherwise or if _component_
            is invalid.
        """
        return cls._service.is_dirty(component)

    @classmethod
    def clean(cls, component: TransformComponent):
        """
        Removes the mark from the component needing to be updated.

        :param component: Any transform component.
        """
        cls._service.clean(component)

    @classmethod
    def get_dirty(cls) -> set[TransformComponent]:
        """
        :return: A set containing all transform components in need of updates.
        """
        return cls._service.get_dirty()

    @classmethod
    def initialize_component(cls, component: TransformComponent, value: Transform):
        """
        Ensures that the transform component is recognized by the service.

        :param component: Any transform component.
        :param value: The starting transform of _component_, in local space.
        """
        cls._service.initialize_component(component, value)
