from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from weakref import WeakSet

from ..types.entity import Entity

if TYPE_CHECKING:
    from ..types._base_type import _BaseType


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
        """
        Returns the number ot active entities managed by the entity manager.
        """
        pass

    @staticmethod
    def get_entity_manager(**kwds) -> EntityManager:
        """
        Extracts an entity manager from keyword arguments.
        Gives the default entity manager if no entity manager is supplied.

        Used for getting an entity manager for a new game instance
        """
        if (entity_manager := kwds.get("entity_manager", None)) is None:
            manager_type = get_default_entity_manager_type()
            entity_manager = manager_type()
        return entity_manager


class DefaultEntityManager(EntityManager):

    def __init__(self) -> None:
        self.entities: WeakSet[Entity] = WeakSet()
        self.new_entities: set[Entity] = set()
        self.disabled_entities: set[Entity] = set()

    def enable(self, item: _BaseType) -> None:
        if isinstance(item, Entity):
            self.new_entities.add(item)

    def disable(self, item: _BaseType) -> None:
        if isinstance(item, Entity):
            self.disabled_entities.add(item)

    def pre_update(self, delta_time: float):
        for entity in self.new_entities:
            self.entities.add(entity)
        self.new_entities = set()
        for entity in self.disabled_entities:
            self.entities.discard(entity)
        self.disabled_entities = set()
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


_default_entity_manager_type = DefaultEntityManager


def get_default_entity_manager_type() -> type[EntityManager]:
    return _default_entity_manager_type


def set_default_entity_manager_type(manager_type: type[EntityManager]):
    global _default_entity_manager_type
    _default_entity_manager_type = manager_type
