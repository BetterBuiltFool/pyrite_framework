from __future__ import annotations

from typing import Protocol, runtime_checkable, TYPE_CHECKING

from .screen_sector import ScreenSector  # noqa: F401
from .camera import CameraBase, Camera  # noqa: F401
from .entity import Entity  # noqa: F401
from .renderable import Renderable  # noqa: F401

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

    def enable(self, item: _BaseType) -> None: ...

    def disable(self, item: _BaseType) -> None: ...


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
