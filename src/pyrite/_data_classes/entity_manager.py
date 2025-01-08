from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from weakref import WeakSet

from src.pyrite.types.entity import Entity

if TYPE_CHECKING:
    from src.pyrite.types._base_type import _BaseType


class EntityManager(ABC):

    @abstractmethod
    def enable(self, item: _BaseType) -> None:
        """
        Adds an entity to the collection of active entities.

        Does nothing if the passed item is not an Entity.

        :param item: Object being enabled. Objects that are not entities will be
        skipped.
        """
        pass

    @abstractmethod
    def disable(self, item: _BaseType) -> None:
        """
        Removes an entity from the collection of active entities.

        Does nothing if the passed item is not an Entity.

        :param item: Object being enabled. Objects that are not entities will be
        skipped.
        """
        pass

    # Update Methods

    @abstractmethod
    def pre_update(self, delta_time: float):
        """
        Runs the pre_update phase for active entities.

        :param delta_time: Time passed since last frame
        """
        pass

    @abstractmethod
    def update(self, delta_time: float):
        """
        Runs the update phase for active entities.

        :param delta_time: Time passed since last frame
        """
        pass

    @abstractmethod
    def post_update(self, delta_time: float):
        """
        Runs the post_update phase for active entities.

        :param delta_time: Time passed since last frame
        """
        pass

    @abstractmethod
    def const_update(self, timestep: float):
        """
        Runs the const_update phase for active entities.

        :param timestep: Length of the simulated step
        """
        pass

    # Profiling methods

    @abstractmethod
    def get_number_entities(self) -> int:
        pass

    @staticmethod
    def get_entity_manager(**kwds) -> EntityManager:
        """
        Extracts an entity manager from keyword arguments.
        Gives the default entity manager if no entity manager is supplied.

        Used for getting an entity manager for a new game instance
        """
        if (entity_manager := kwds.get("entity_manager", None)) is None:
            entity_manager = DefaultEntityManager()
        return entity_manager


class DefaultEntityManager(EntityManager):

    def __init__(self) -> None:
        self.entities: WeakSet[Entity] = WeakSet()

    def enable(self, item: _BaseType) -> None:
        if isinstance(item, Entity):
            self.entities.add(item)

    def disable(self, item: _BaseType) -> None:
        if isinstance(item, Entity):
            self.entities.discard(item)

    def pre_update(self, delta_time: float):
        for entity in self.entities:
            entity.pre_update(delta_time)

    def update(self, delta_time: float):
        for entity in self.entities:
            entity.update(delta_time)

    def post_update(self, delta_time: float):
        for entity in self.entities:
            entity.post_update(delta_time)

    def const_update(self, timestep: float):
        for entity in self.entities:
            entity.const_update(timestep)

    def get_number_entities(self) -> int:
        return len(self.entities)
