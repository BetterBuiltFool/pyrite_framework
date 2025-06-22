from __future__ import annotations

from typing import TYPE_CHECKING

from ...types.service import ServiceProvider

from .bounds_service import BoundsService, DefaultBoundsService

if TYPE_CHECKING:
    pass


class BoundsServiceProvider(ServiceProvider):
    _service: BoundsService = DefaultBoundsService()

    @classmethod
    def hotswap(cls, service: BoundsService):
        return super().hotswap(service)
