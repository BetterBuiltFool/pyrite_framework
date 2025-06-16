from __future__ import annotations

from abc import abstractmethod
from types import ModuleType

from ..types import System
from .transform import Transform
from . import transform_service as ts


transform_service: ModuleType = ts  # Default to pyrite.transform.transform_service


class TransformSystem(System):

    @staticmethod
    def to_world(transform: Transform, context: Transform) -> Transform:
        """
        :param transform: A Transform in local space
        :param context: A Transform representing the local space of _transform_,
            in world space
        :return: Equivalent to _transform_, in world space.
        """
        pass

    @staticmethod
    def to_local(transform: Transform, context: Transform) -> Transform:
        """
        :param transform: A Transform in world space
        :param context: A Transform representing the local space _transform_ is being
            converted to, in world space
        :return: Equivalent to _transform_, in local space.
        """
        pass

    @staticmethod
    @abstractmethod
    def convert_to_world(transform: Transform) -> Transform:
        """
        Converts the transform into world space, with context defined by the system
        implementation.

        :param transform: A Transform object in local space.
        :return: A Transform that represents _transform_ in world space.
        """
        pass

    @staticmethod
    @abstractmethod
    def convert_to_local(transform: Transform) -> Transform:
        """
        Converts the transform into local space, with context defined by the system
        implementation.

        :param transform: A Transform object in world space.
        :return: A Transform that represents _transform_ in local space.
        """
        pass


class DefaultTransformSystem(TransformSystem):
    """
    Simple TransformSystem that doesn't differentiate between world and local
    transforms.
    """

    @staticmethod
    def convert_to_world(transform: Transform) -> Transform:
        return transform

    @staticmethod
    def convert_to_local(transform: Transform) -> Transform:
        return transform

    def pre_render(self, delta_time: float) -> None:
        for component in transform_service.get_dirty():
            transform = transform_service.get_local(component)
            transform_service.set_world(component, transform.copy())
            transform_service.clean(component)


_default_transform_system: type[TransformSystem] = DefaultTransformSystem


def get_default_transform_system_type() -> type[TransformSystem]:
    """
    :return: The class of the target Transform system
    """
    return _default_transform_system


def set_default_transform_system_type(system_type: type[TransformSystem]):
    """
    Sets the default transform system.

    :param system_type: A type that is a subclass of TransformSystem
    """
    global _default_transform_system
    _default_transform_system = system_type


def set_transform_service(module: ModuleType):
    global transform_service
    transform_service = module
