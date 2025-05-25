from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class DebugRenderer(ABC):

    @abstractmethod
    def render(self, *args, **kwds):
        """
        Generic render function.
        Passed parameters vary depending on where the renderer gets called.
        """
        pass
