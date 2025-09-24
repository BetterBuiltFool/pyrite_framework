from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING
from weakref import WeakKeyDictionary

from pyrite._types.service import Service

if TYPE_CHECKING:
    from pyrite._types.bounds import CullingBounds
    from pyrite._types.renderable import Renderable
    from pyrite._types.protocols import TransformLike

    type BoundsData = tuple[CullingBounds, TransformLike]


class BoundsService(Service):

    @abstractmethod
    def get(self, renderable: Renderable) -> BoundsData | tuple[None, None]:
        pass

    @abstractmethod
    def set(self, renderable: Renderable, data: BoundsData):
        pass


class DefaultBoundsService(BoundsService):

    def __init__(self) -> None:
        self._renderables: WeakKeyDictionary[Renderable, BoundsData] = (
            WeakKeyDictionary()
        )

    def get(self, renderable: Renderable) -> BoundsData | tuple[None, None]:
        return self._renderables.get(renderable, (None, None))

    def set(self, renderable: Renderable, data: BoundsData):
        self._renderables[renderable] = data

    def transfer(self, target_service: BoundsService):
        for renderable, data in self._renderables.items():
            target_service.set(renderable, data)
