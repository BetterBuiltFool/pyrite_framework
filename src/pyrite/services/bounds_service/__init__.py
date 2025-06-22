from __future__ import annotations

from typing import TYPE_CHECKING

from ...types.service import ServiceProvider

from .bounds_service import BoundsService, DefaultBoundsService

if TYPE_CHECKING:
    from ...types import Renderable
    from .bounds_service import BoundsData


class BoundsServiceProvider(ServiceProvider):
    _service: BoundsService = DefaultBoundsService()

    @classmethod
    def hotswap(cls, service: BoundsService):
        return super().hotswap(service)

    # -----------------------Delegates-----------------------

    @classmethod
    def get(cls, renderable: Renderable) -> BoundsData | tuple[None, None]:
        return cls._service.get(renderable)

    @classmethod
    def set(cls, renderable: Renderable, data: BoundsData):
        cls._service.set(renderable, data)
