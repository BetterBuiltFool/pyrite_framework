from __future__ import annotations
from typing import Protocol, TYPE_CHECKING

import pygame

import pyrite._types.bounds
import pyrite._types.camera
import pyrite._types.component
import pyrite._types.debug_renderer
import pyrite._types.entity
import pyrite._types.projection
import pyrite._types.renderable
import pyrite._types.renderer
import pyrite._types.sprite
import pyrite._types.system
import pyrite._types.transform
import pyrite._types.view_bounds

if TYPE_CHECKING:
    from pygame import Surface
    from pygame.typing import SequenceLike

    from pyrite._transform.transform_component import TransformComponent

    Point3D = SequenceLike[float]

CullingBounds = pyrite._types.bounds.CullingBounds
Camera = pyrite._types.camera.CameraBase
Component = pyrite._types.component.Component
DebugRenderer = pyrite._types.debug_renderer.DebugRenderer
Entity = pyrite._types.entity.Entity
Projection = pyrite._types.projection.Projection
Renderable = pyrite._types.renderable.Renderable
Renderer = pyrite._types.renderer.Renderer
RendererProvider = pyrite._types.renderer.RendererProvider
Sprite = pyrite._types.sprite.BaseSprite
System = pyrite._types.system.System
TransformLike = pyrite._types.transform.TransformLike
CameraViewBounds = pyrite._types.view_bounds.CameraViewBounds


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
