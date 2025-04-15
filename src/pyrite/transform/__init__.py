from __future__ import annotations
from types import ModuleType

from .transform import Transform  # noqa:F401
from . import transform_component, transform_system
from .transform_component import TransformComponent  # noqa:F401

from .transform_system import TransformSystem  # noqa:F401


def set_transform_service(module: ModuleType):
    transform_component.set_transform_service(module)
    transform_system.set_transform_service(module)
