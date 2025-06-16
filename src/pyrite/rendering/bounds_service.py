from __future__ import annotations

from typing import TypeAlias, TYPE_CHECKING
from weakref import WeakKeyDictionary

if TYPE_CHECKING:
    from ..types import CullingBounds, Renderable, Transform

    BoundsData: TypeAlias = tuple[CullingBounds, Transform]


class BoundsService:
    """
    A services that tracks and store data for the Bounds of renderables.
    """

    _renderables: WeakKeyDictionary[Renderable, BoundsData] = WeakKeyDictionary()

    @classmethod
    def get(cls, renderable: Renderable) -> BoundsData | tuple[None, None]:
        return cls._renderables.get(renderable, (None, None))

    @classmethod
    def set(cls, renderable: Renderable, data: BoundsData):
        cls._renderables.update({renderable: data})
