from __future__ import annotations

from abc import abstractmethod
from typing import TypeAlias, TYPE_CHECKING
from weakref import WeakKeyDictionary

from ...types.service import Service

if TYPE_CHECKING:
    from ...types import CullingBounds, Renderable, Transform

    BoundsData: TypeAlias = tuple[CullingBounds, Transform]


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
        self._renderables.update({renderable: data})
