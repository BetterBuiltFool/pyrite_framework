from __future__ import annotations

from typing import Protocol, runtime_checkable, TYPE_CHECKING

if TYPE_CHECKING:
    from pygame import Vector2


@runtime_checkable
class TransformProtocol(Protocol):
    position: Vector2
    rotation: float
    scale: Vector2
