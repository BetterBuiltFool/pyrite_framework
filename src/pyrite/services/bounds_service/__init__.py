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
        cls._service.transfer(service)
        cls._service = service

    # -----------------------Delegates-----------------------

    @classmethod
    def get(cls, renderable: Renderable) -> BoundsData | tuple[None, None]:
        """
        Gets the bounds data for a given renderable, if it exists.

        :param renderable: A Renderable whose bounds data is to be fetched.
        :return: The renderable's data, or (None, None) if not available.
        """
        return cls._service.get(renderable)

    @classmethod
    def set(cls, renderable: Renderable, data: BoundsData):
        """
        Sets the bounds data for a given renderable

        :param renderable: The Renderable whose data is being set.
        :param data: The new data for the renderable
        """
        cls._service.set(renderable, data)
