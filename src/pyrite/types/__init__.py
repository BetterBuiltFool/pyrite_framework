from __future__ import annotations

from typing import Protocol, runtime_checkable, TYPE_CHECKING

from .camera import CameraBase  # noqa: F401
from .entity import Entity  # noqa: F401
from .enums import RenderLayers, AnchorPoint, Layer, Anchor  # noqa: F401
from .renderable import Renderable  # noqa: F401
from .sprite import Sprite  # noqa: F401
from .spritesheet import SpriteSheet, SpriteMap  # noqa: F401
from .surface_sector import SurfaceSector  # noqa: F401
from .static_decor import StaticDecor  # noqa: F401
from .system import System  # noqa: F401
from .transform import TransformProtocol  # noqa:F401

# TODO Shift most of these out into core, and keep these references for typechecking
# only

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
