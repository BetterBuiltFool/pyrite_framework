from __future__ import annotations

from typing import Protocol, runtime_checkable, TYPE_CHECKING

from .bounds import CullingBounds  # noqa: F401
from .camera import CameraBase  # noqa: F401
from .component import Component  # noqa: F401
from .entity import Entity  # noqa: F401
from .renderable import Renderable  # noqa: F401
from .renderer import Renderer  # noqa: F401
from .system import System  # noqa: F401
from .transform import TransformProtocol  # noqa:F401
from .view_bounds import CameraViewBounds  # noqa: F401

if TYPE_CHECKING:
    from pygame import Surface
    from pygame.typing import Point, SequenceLike
    from ..transform import Transform

    Point3D = SequenceLike[float]

import pygame


@runtime_checkable
class Container(Protocol):
    """
    An object that can forward Entities and Renderables to the active EntityManager and
    RenderManager for enabling and disabling.
    """

    container: Container
    """
    A Container for the container. Needs to loop back into the game class eventually.
    """


class HasPosition(Protocol):
    """
    Describes an object that has a Vector2 position attribute.
    """

    position: pygame.Vector2
    """
    The location of the item, either in world space or local space.
    """


class HasTransform(Protocol):
    transform: Transform


class HasTexture(Protocol):

    @property
    def texture(self) -> Surface:
        pass

    @property
    def is_dirty(self) -> bool:
        pass


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


class TransformDependent(Protocol):
    """
    Defines hooks for classes that require update from a TransformComponent's world
    values.
    """

    def world_position_changed(self, world_position: Point):
        """
        Called whenever the world position of the TransformComponent is set.

        :param world_position: The updated world position of the TransformComponent
        """

    def world_scale_changed(self, world_scale: Point):
        """
        Called whenever the world scale of the TransformComponent is set.

        :param world_scale: The updated world scale of the TransformComponent
        """

    def world_rotation_changed(self, world_rotation: float):
        """
        Called whenever the world rotation of the TransformComponent is set.

        :param world_rotation: The updated world position of the TransformComponent
        """
