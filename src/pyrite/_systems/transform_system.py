from __future__ import annotations

from typing import TYPE_CHECKING

from pyrite._services.transform_service import (
    TransformServiceProvider as TransformService,
)
from pyrite._systems.base_system import BaseSystem


if TYPE_CHECKING:
    pass


class TransformSystem(BaseSystem):
    """
    System for ensuring that TransformComponent world values are up to date for
    rendering.
    """

    def pre_render(self) -> None:
        TransformService.frame_reset()
        for component in TransformService.traverse_transforms():
            assert component
            if not component.is_dirty():
                continue

            # We need to mark all descending nodes as dirty, since they are depending
            # on this node.
            for subcomponent in TransformService.get_dependents(component):
                TransformService.make_dirty(subcomponent)
            TransformService.clean(component)


_default_transform_system: type[TransformSystem] = TransformSystem


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
