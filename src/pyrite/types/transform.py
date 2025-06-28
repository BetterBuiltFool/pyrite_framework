from __future__ import annotations

from typing import Protocol, runtime_checkable, TYPE_CHECKING

if TYPE_CHECKING:
    from pygame import Vector2
    from pygame.typing import Point


@runtime_checkable
class TransformLike(Protocol):

    @property
    def position(self) -> Vector2: ...

    @position.setter
    def position(self, new_position: Point): ...

    @property
    def rotation(self) -> float: ...

    @rotation.setter
    def rotation(self, angle: float): ...

    @property
    def scale(self) -> Vector2: ...

    @scale.setter
    def scale(scale, new_scale: Point): ...
