from __future__ import annotations

from typing import TYPE_CHECKING

from .physics_service import PhysicsService, PymunkPhysicsService
from ...types.service import ServiceProvider

if TYPE_CHECKING:
    pass


class PhysicsServiceProvider(ServiceProvider):
    _service: PhysicsService = PymunkPhysicsService()

    @classmethod
    def hotswap(cls, service: PhysicsService):
        cls._service.transfer(service)
        cls._service = service
