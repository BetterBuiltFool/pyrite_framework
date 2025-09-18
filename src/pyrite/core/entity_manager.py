from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Self, TYPE_CHECKING

from weakref import WeakSet


if TYPE_CHECKING:
    from pyrite._types.entity import Entity

import pygame


_active_entity_manager: EntityManager


def get_entity_manager() -> EntityManager:
    return _active_entity_manager


def set_entity_manager(manager: EntityManager):
    global _active_entity_manager
    _active_entity_manager = manager


_deferred_enables: set[Entity] = set()


def enable(entity: Entity):
    """
    Enables an entity with the active entity manager.
    If no active entity manager exists, the entity is stored until one is created.

    :param entity: An entity to be enabled.
    """
    if _active_entity_manager:

        return _active_entity_manager.enable(entity)
    _deferred_enables.add(entity)


def disable(entity: Entity):
    """
    Disables an entity in the active entity manager,
    If no active entity manager exists and the entity is queued for enabling,
    it is removed from the queue.

    :param entity: An entity to be disabled.
    """
    if _active_entity_manager:
        _active_entity_manager.disable(entity)
        return
    _deferred_enables.discard(entity)


def is_enabled(entity: Entity) -> bool:
    """
    Determines if the passed entity is currently considered enabled by the manager.

    :param item: Any entity
    :return: True if currently enabled, False if disabled
    """
    if not _active_entity_manager:
        return False
    return _active_entity_manager.is_enabled(entity)


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
    def enable(self, item: Entity) -> bool:
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
    def disable(self, item: Entity) -> bool:
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
    def is_enabled(self, item: Entity) -> bool:
        """
        Determines if the passed entity is currently considered enabled by the manager.

        :param item: Any entity
        :return: True if currently enabled, False if disabled
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

    def enable(self, item: Entity) -> bool:
        if item in self._disabled_buffer:
            self._disabled_buffer.remove(item)
        else:
            self._added_buffer.add(item)
        return item not in self.entities

    def disable(self, item: Entity) -> bool:
        if item in self._added_buffer:
            self._added_buffer.remove(item)
        else:
            self._disabled_buffer.add(item)
        return item in self.entities

    def is_enabled(self, item: Entity) -> bool:
        return item in self._added_buffer or (
            item in self.entities and item not in self._disabled_buffer
        )

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
