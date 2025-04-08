from __future__ import annotations

from abc import ABC
from typing import Protocol, runtime_checkable, TYPE_CHECKING

from .camera import CameraBase, Camera, ChaseCamera  # noqa: F401
from .entity import Entity  # noqa: F401
from .enums import RenderLayers, AnchorPoint, Layer, Anchor  # noqa: F401
from .renderable import Renderable  # noqa: F401
from .sprite import Sprite  # noqa: F401
from .spritesheet import SpriteSheet, SpriteMap  # noqa: F401
from .surface_sector import SurfaceSector  # noqa: F401
from .static_decor import StaticDecor  # noqa: F401
from .system import System  # noqa: F401
from .. import game

if TYPE_CHECKING:
    from ._base_type import _BaseType

import pygame


@runtime_checkable
class Container(Protocol):
    """
    An object that can forward Entities and Renderables to the active EntityManager and
    Renderer for enabling and disabling.
    """

    container: Container
    """
    A Container for the container. Needs to loop back into the game class eventually.
    """

    def enable(self, item: _BaseType) -> bool: ...

    def disable(self, item: _BaseType) -> bool: ...


class HasPosition(Protocol):
    """
    Describes an object that has a Vector2 position attribute.
    """

    position: pygame.Vector2
    """
    The location of the item, either in world space or local space.
    """


class SystemManagable(ABC):

    def add_to_system(self, system_type: type[System]):
        if system := self.get_system(system_type):
            system.register(self)

    def remove_from_system(self, system_type: type[System]):
        if system := self.get_system(system_type):
            system.deregister(self)

    def get_system(self, system_type: type[System]) -> System | None:
        system_manager = game.get_system_manager()
        return system_manager.get_system(system_type)


class CanUpdate(Protocol):

    def update(self, delta_time: float) -> None: ...


class CanPreUpdate(Protocol):

    def pre_update(self, delta_time: float) -> None: ...


class CanPostUpdate(Protocol):

    def post_update(self, delta_time: float) -> None: ...


class CanConstUpdate(Protocol):

    def const_update(self, timestep: float) -> None: ...


class CanRender(Protocol):

    def render(self, delta_time: float) -> tuple[pygame.Surface, pygame.Rect]: ...
