from __future__ import annotations

from typing import Protocol, runtime_checkable, TYPE_CHECKING


if TYPE_CHECKING:
    from pygame import Rect, Surface, Vector2
    from pygame.typing import Point
    from pyrite._component.transform_component import TransformComponent


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

    def update(self) -> None: ...


class CanPreUpdate(Protocol):

    def pre_update(self) -> None: ...


class CanPostUpdate(Protocol):

    def post_update(self) -> None: ...


class CanConstUpdate(Protocol):

    def const_update(self) -> None: ...


class RenderTarget(Protocol):

    def get_target_surface(self) -> Surface:
        """
        Gets the surface to be drawn to.
        """
        ...

    def get_target_rect(self) -> Rect:
        """
        Gets the Rect that represents the surface space of the RenderTarget.
        """
        ...

    @property
    def crop(self) -> bool:
        """
        Determines if the rendering should be cropped or not.
        If False, the rendering will be scaled to fit the target.
        """
        ...


@runtime_checkable
class TransformLike(Protocol):

    @property
    def position(self) -> Vector2: ...

    @position.setter
    def position(self, position: Point): ...

    @property
    def rotation(self) -> float: ...

    @rotation.setter
    def rotation(self, rotation: float): ...

    @property
    def scale(self) -> Vector2: ...

    @scale.setter
    def scale(self, scale: Point): ...
