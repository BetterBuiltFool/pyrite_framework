from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Self, TYPE_CHECKING

from weakref import WeakSet

from ..types.entity import Entity

if TYPE_CHECKING:
    from ..types._base_type import _BaseType

import pygame


_active_entity_manager: EntityManager = None


def get_entity_manager() -> EntityManager:
    return _active_entity_manager


def set_entity_manager(manager: EntityManager):
    global _active_entity_manager
    _active_entity_manager = manager


_deferred_enables: set[Entity] = set()


def enable(entity: Entity):
    if _active_entity_manager:
        _active_entity_manager.enable(entity)
        return
    _deferred_enables.add(entity)


def disable(entity: Entity):
    if _active_entity_manager:
        _active_entity_manager.disable(entity)
        return
    _deferred_enables.discard(entity)


class EntityManager(ABC):

    def __new__(cls) -> Self:
        new_manager = super().__new__(cls)
        set_entity_manager(new_manager)
        return new_manager

    def __init__(self) -> None:
        # Subclasses must call super().__init__ at the END of initialization
        for entity in _deferred_enables:
            self.enable(entity)

    @abstractmethod
    def enable(self, item: _BaseType) -> bool:
        """
        Adds an entity to the collection of active entities.

        Does nothing if the passed item is not an Entity.

        :param item: Object being enabled. Objects that are not entities will be
        skipped.
        :return: True if enable is successful, False if not, such as object already
        enabled.
        """
        pass

    @abstractmethod
    def disable(self, item: _BaseType) -> bool:
        """
        Removes an entity from the collection of active entities.

        Does nothing if the passed item is not an Entity.

        :param item: Object being enabled. Objects that are not entities will be
        skipped.
        :return: True if disable is successful, False if not, such as object already
        disabled.
        """
        pass

    @abstractmethod
    def flush_buffer(self):
        """
        Used to allow the entity manager to update its entity collection safely,
        without modifying it while iterating over it.

        Called at the beginning of the loop, before event handling.
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

    @abstractmethod
    def handle_event(self, event: pygame.Event):
        """
        Passes the event down to all active entities.

        :param event: A pygame event.
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
        self._added_buffer: set[Entity] = set()
        self._disabled_buffer: set[Entity] = set()

        super().__init__()

    def enable(self, item: _BaseType) -> bool:
        if isinstance(item, Entity):
            if item in self._disabled_buffer:
                self._disabled_buffer.remove(item)
            else:
                self._added_buffer.add(item)
            return item not in self.entities
        return False

    def disable(self, item: _BaseType) -> bool:
        if isinstance(item, Entity):
            if item in self._added_buffer:
                self._added_buffer.remove(item)
            else:
                self._disabled_buffer.add(item)
            return item in self.entities
        return False

    def flush_buffer(self):
        self.entities |= self._added_buffer

        self.entities -= self._disabled_buffer

        self._added_buffer = set()
        self._disabled_buffer = set()

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

    def handle_event(self, event: pygame.Event):
        for entity in self.entities:
            entity.on_event(event)

    def get_number_entities(self) -> int:
        return len(self.entities)


_default_entity_manager_type = DefaultEntityManager


def get_default_entity_manager_type() -> type[EntityManager]:
    return _default_entity_manager_type


def set_default_entity_manager_type(manager_type: type[EntityManager]):
    global _default_entity_manager_type
    _default_entity_manager_type = manager_type
