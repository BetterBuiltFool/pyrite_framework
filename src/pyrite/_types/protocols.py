from __future__ import annotations

from typing import Protocol, TYPE_CHECKING


if TYPE_CHECKING:
    from pygame import Surface, Vector2
    from pyrite._transform.transform_component import TransformComponent


class HasPosition(Protocol):
    """
    Describes an object that has a Vector2 position attribute.
    """

    position: Vector2
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
