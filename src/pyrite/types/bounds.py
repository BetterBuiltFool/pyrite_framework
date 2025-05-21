from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygame.typing import Point


class CullingBounds(ABC):

    @abstractmethod
    def get_volume(self) -> list[Point]:
        pass

    @abstractmethod
    def flatten(self) -> list[Point]:
        pass
