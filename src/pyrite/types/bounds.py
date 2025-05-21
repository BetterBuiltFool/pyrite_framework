from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygame.typing import Point


class Bounds(ABC):

    @abstractmethod
    def get_bounds(self) -> list[Point]:
        pass
