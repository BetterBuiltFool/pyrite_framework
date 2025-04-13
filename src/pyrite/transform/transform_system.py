from __future__ import annotations

from abc import abstractmethod

from ..types import System
from .transform import Transform


class TransformSystem(System):

    @abstractmethod
    def to_world(self, transform: Transform, context: Transform) -> Transform:
        pass

    @abstractmethod
    def to_local(self, transform: Transform, context: Transform) -> Transform:
        pass
