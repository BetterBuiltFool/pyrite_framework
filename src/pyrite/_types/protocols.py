from __future__ import annotations

from typing import Generic, Protocol, runtime_checkable, TYPE_CHECKING, TypeVar


if TYPE_CHECKING:
    from collections.abc import Callable
    from pygame import Rect, Surface, Vector2
    from pygame.typing import Point

    import glm

    # from pyrite._component.transform_component import TransformComponent
    from pyrite.types import CubeLike, TransformLike

T_contra = TypeVar("T_contra", contravariant=True)


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

    transform: TransformLike


class HasTransformProperty(Protocol):
    """
    An object with a TransformComponent property called _transform_.
    """

    @property
    def transform(self) -> TransformLike | Callable[[], TransformLike]: ...


class HasTexture(Protocol):
    texture: Surface
    is_dirty: bool


class _HasCuboidAttribute(Protocol):
    """
    An object that has an attribute that is either a Cuboid,
    or a function that returns a Cuboid.
    """

    @property
    def cuboid(self) -> CubeLike | Callable[[], CubeLike]: ...


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

    # @property
    # def crop(self) -> bool:
    #     """
    #     Determines if the rendering should be cropped or not.
    #     If False, the rendering will be scaled to fit the target.
    #     """
    #     ...


@runtime_checkable
class HasTransformAttributes(Protocol):

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

    @property
    def matrix(self) -> glm.mat4x4: ...


class Manager(Generic[T_contra], Protocol):
    """
    Protocol for a class that handles Enableables.

    Managers should be static, but may wrap an instance that does the actual work.

    Managers are responsible for calling OnEnable and OnDisable events, as well as
    on_enable and on_disable hooks.

    The enableables themselves call on_preenable and on_predisable.
    """

    @classmethod
    def enable(cls, item: T_contra) -> None: ...

    @classmethod
    def disable(cls, item: T_contra) -> None: ...

    @classmethod
    def is_enabled(cls, item: T_contra) -> bool: ...
