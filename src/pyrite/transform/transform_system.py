from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from ..services import TransformService
from ..systems import System
from .transform import Transform


if TYPE_CHECKING:
    from .transform_component import TransformComponent


class TransformSystem(System):

    # @staticmethod
    # def to_world(transform: Transform, context: Transform) -> Transform:
    #     """
    #     :param transform: A Transform in local space
    #     :param context: A Transform representing the local space of _transform_,
    #         in world space
    #     :return: Equivalent to _transform_, in world space.
    #     """
    #     pass

    # @staticmethod
    # def to_local(transform: Transform, context: Transform) -> Transform:
    #     """
    #     :param transform: A Transform in world space
    #     :param context: A Transform representing the local space _transform_ is being
    #         converted to, in world space
    #     :return: Equivalent to _transform_, in local space.
    #     """
    #     pass

    @staticmethod
    @abstractmethod
    def convert_to_world(transform: TransformComponent) -> Transform:
        """
        Converts the transform component into world space, with context defined by the
        system implementation.

        :param transform: A TransformComponent object.
        :return: A Transform that represents the world space value of _transform_.
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
    def convert_to_world(transform: TransformComponent) -> Transform:
        if not (parent := TransformService.get_relative_of(transform)):
            # We are dealing with a root component
            return transform.raw().copy()

        return parent.world() * transform

    @staticmethod
    def convert_to_local(transform: Transform) -> Transform:
        return transform

    def pre_render(self, delta_time: float) -> None:
        for component in TransformService.traverse_transforms():
            assert component
            if not component.is_dirty():
                continue

            # We need to mark all descending nodes as dirty, since they are depending
            # on this node.
            for subcomponent in TransformService.get_dependents(component):
                TransformService.make_dirty(subcomponent)
            TransformService.clean(component)


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
