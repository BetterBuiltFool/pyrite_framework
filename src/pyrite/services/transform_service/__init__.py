from __future__ import annotations

from typing import TYPE_CHECKING
from weakref import WeakSet

from ...types.service import ServiceProvider
from ...transform import Transform, TransformComponent
from .transform_service import TransformService as _TransformService

if TYPE_CHECKING:
    from pygame.typing import Point


class TransformService(ServiceProvider):
    """
    Service that contains and maintains data for TransformComponents
    """

    _service: _TransformService

    dirty_components: WeakSet[TransformComponent] = WeakSet()

    @classmethod
    def hotswap(cls, service: _TransformService):
        cls._service.transfer(service)
        cls._service = service

    @classmethod
    def get_local(cls, component: TransformComponent) -> Transform:
        """
        :param component: Any transform component.
        :return: The Transform object representing _component_ in local space.
        """
        pass

    @classmethod
    def get_local_position(cls, component: TransformComponent) -> Point:
        """
        :param component: Any transform component.
        :return: The current position of _component_, in local space.
        """
        pass

    @classmethod
    def get_local_rotation(cls, component: TransformComponent) -> float:
        """
        :param component: Any transform component.
        :return: The current rotation of _component_, in local space.
        """
        pass

    @classmethod
    def get_local_scale(cls, component: TransformComponent) -> Point:
        """
        :param component: Any transform component.
        :return: The current scaling factor of _component_, in local space.
        """
        pass

    @classmethod
    def set_local(cls, component: TransformComponent, value: Transform):
        """
        Forces the local transform value of a transform component to a new value.
        Does not mark the component for updates.

        :param component: Any transform component.
        :param value: A Transform value, in local space.
        """
        pass

    @classmethod
    def set_local_position(cls, component: TransformComponent, position: Point):
        """
        Sets the position of the transform component to the new position.
        The component will be marked for updating.

        :param component: Any transform component.
        :param position: A point in local space.
        """
        pass

    @classmethod
    def set_local_rotation(cls, component: TransformComponent, angle: Point):
        """
        Sets the rotation of the transform component to the new rotation.
        The component will be marked for updating.

        :param component: Any transform component.
        :param angle: An angle in local space.
        """
        pass

    @classmethod
    def set_local_scale(cls, component: TransformComponent, scale: Point):
        """
        Sets the scale of the transform component to the new scaling factor.
        The component will be marked for updating.

        :param component: Any transform component.
        :param position: A tuple with scaling factors for each dimension, in local
            space.
        """
        pass

    @classmethod
    def get_world(cls, component: TransformComponent) -> Transform:
        """
        :param component: Any transform component.
        :return: A Transform object representing _component_ in world space.
        """
        pass

    @classmethod
    def get_world_position(cls, component: TransformComponent) -> Point:
        """
        :param component: Any transform component.
        :return: The current position of _component_, in world space.
        """
        pass

    @classmethod
    def get_world_rotation(cls, component: TransformComponent) -> float:
        """
        :param component: Any transform component.
        :return: The current rotation of _component_, in world space.
        """
        pass

    @classmethod
    def get_world_scale(cls, component: TransformComponent) -> Point:
        """
        :param component: Any transform component.
        :return: The current scaling factor of _component_, in world space.
        """
        pass

    @classmethod
    def set_world(cls, component: TransformComponent, value: Transform):
        """
        Forces the world transform value of a transform component to a new value.


        :param component: Any transform component.
        :param value: A Transform value, in world space.
        """
        pass

    @classmethod
    def set_world_position(cls, component: TransformComponent, position: Point):
        """
        Sets the position of the transform component to the new position.
        The component will be marked for updating.

        :param component: Any transform component.
        :param position: A point in world space.
        """
        pass

    @classmethod
    def set_world_rotation(cls, component: TransformComponent, angle: Point):
        """
        Sets the rotation of the transform component to the new rotation.
        The component will be marked for updating.

        :param component: Any transform component.
        :param angle: An angle in world space.
        """
        pass

    @classmethod
    def set_world_scale(cls, component: TransformComponent, scale: Point):
        """
        Sets the scale of the transform component to the new scaling factor.
        The component will be marked for updating.

        :param component: Any transform component.
        :param position: A tuple with scaling factors for each dimension, in world
            space.
        """
        pass

    @classmethod
    def is_dirty(cls, component: TransformComponent) -> bool:
        """
        Checks if a transform component is in need of updating.

        :param component: Any transform component.
        :return: True if _component_ needs cleaning, False otherwise or if _component_
            is invalid.
        """
        pass

    @classmethod
    def clean(cls, component: TransformComponent):
        """
        Removes the mark from the component needing to be updated.

        :param component: Any transform component.
        """
        pass

    @classmethod
    def get_dirty(cls) -> set[TransformComponent]:
        """
        :return: A set containing all transform components in need of updates.
        """
        pass

    @classmethod
    def initialize_component(cls, component: TransformComponent, value: Transform):
        """
        Ensures that the transform component is recognized by the service.

        :param component: Any transform component.
        :param value: The starting transform of _component_, in local space.
        """
        pass
