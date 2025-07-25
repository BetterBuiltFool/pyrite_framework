from __future__ import annotations

from typing import Protocol, TYPE_CHECKING

from .bounds import CullingBounds  # noqa: F401
from .camera import CameraBase as Camera  # noqa: F401
from .component import Component  # noqa: F401
from .debug_renderer import DebugRenderer  # noqa: F401
from .entity import Entity  # noqa: F401
from .projection import Projection  # noqa: F401
from .renderable import Renderable  # noqa: F401
from .renderer import Renderer, RendererProvider  # noqa: F401
from .sprite import BaseSprite as Sprite  # noqa: F401
from .system import System  # noqa: F401
from .transform import TransformLike  # noqa:F401
from .view_bounds import CameraViewBounds  # noqa: F401

if TYPE_CHECKING:
    from pygame import Surface
    from pygame.typing import SequenceLike
    from ..transform.transform_component import TransformComponent

    Point3D = SequenceLike[float]

import pygame


class HasPosition(Protocol):
    """
    Describes an object that has a Vector2 position attribute.
    """

    position: pygame.Vector2
    """
    The location of the item, either in world space or local space.
    """


class HasTransform(Protocol):
    """
    An object with a TransformComponent attribute called _transform_.
    """

    transform: TransformComponent


class HasTransformProperty(Protocol):
    """
    An object with a TransformComponent property called _transform_.
    """

    @property
    def transform(self) -> TransformComponent: ...

    @transform.setter
    def transform(self, value: TransformComponent) -> None: ...


class HasTexture(Protocol):
    texture: Surface
    is_dirty: bool


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
