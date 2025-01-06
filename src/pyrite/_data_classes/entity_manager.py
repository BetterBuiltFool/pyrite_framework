from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from weakref import WeakSet

from src.pyrite.types.entity import Entity
from src.pyrite.types.service import Service

if TYPE_CHECKING:
    from src.pyrite.types._base_type import _BaseType
    from src.pyrite.game import Game


class EntityManager(ABC):

    def __init__(self, game_instance: Game) -> None:
        self.game_instance = game_instance

    @abstractmethod
    def enable(self, item: _BaseType) -> None:
        pass

    @abstractmethod
    def disable(self, item: _BaseType) -> None:
        pass

    # Update Methods

    @abstractmethod
    def pre_update(self, delta_time: float):
        pass

    @abstractmethod
    def update(self, delta_time: float):
        pass

    @abstractmethod
    def post_update(self, delta_time: float):
        pass

    @abstractmethod
    def const_update(self, timestep: float):
        pass

    @staticmethod
    def get_entity_manager(game_instance: Game, **kwds) -> EntityManager:
        if (entity_manager := kwds.get("entity_manager", None)) is None:
            entity_manager = DefaultEntityManager(game_instance)
        return entity_manager


class DefaultEntityManager(EntityManager):

    def __init__(self, game_instance: Game) -> None:
        super().__init__(game_instance)
        self.entities: WeakSet[Entity] = WeakSet()
        self.services: WeakSet[Service] = WeakSet()

    def enable(self, item: _BaseType) -> None:
        if isinstance(item, Entity):
            self.entities.add(item)
        elif isinstance(item, Service):
            self.services.add(item)

    def disable(self, item: _BaseType) -> None:
        if isinstance(item, Entity):
            self.entities.discard(item)
        elif isinstance(item, Service):
            self.services.discard(item)

    def pre_update(self, delta_time: float):
        for service in self.services:
            service.pre_update(delta_time)
        for entity in self.entities:
            entity.pre_update(delta_time)

    def update(self, delta_time: float):
        for service in self.services:
            service.update(delta_time)
        for entity in self.entities:
            entity.update(delta_time)

    def post_update(self, delta_time: float):
        for service in self.services:
            service.post_update(delta_time)
        for entity in self.entities:
            entity.post_update(delta_time)

    def const_update(self, timestep: float):
        for service in self.services:
            service.const_update(timestep)
        for entity in self.entities:
            entity.const_update(timestep)
