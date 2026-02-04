from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Self, TYPE_CHECKING

from weakref import WeakSet


if TYPE_CHECKING:
    from pyrite._types.entity import Entity

import pygame


_deferred_enables: set[Entity] = set()


class EntityManager:
    _active_entity_manager: AbstractEntityManager

    @classmethod
    def enable(cls, item: Entity) -> bool:
        """
        Adds an entity to the collection of active entities.

        Does nothing if the passed item is not an Entity.

        :param item: Object being enabled. Objects that are not entities will be
        skipped.
        :return: True if enable is successful, False if not, such as object already
        enabled.
        """
        # Only runs when a proper entity manager doesn't exist yet
        flag = item not in _deferred_enables
        _deferred_enables.add(item)
        return flag

    @classmethod
    def _enable_wrapper(cls, item: Entity) -> bool:
        return cls._active_entity_manager.enable(item)

    @classmethod
    def disable(cls, item: Entity) -> bool:
        """
        Removes an entity from the collection of active entities.

        Does nothing if the passed item is not an Entity.

        :param item: Object being enabled. Objects that are not entities will be
        skipped.
        :return: True if disable is successful, False if not, such as object already
        disabled.
        """
        # Only runs when a proper entity manager doesn't exist yet
        flag = item in _deferred_enables
        _deferred_enables.discard(item)
        return flag

    @classmethod
    def _disable_wrapper(cls, item: Entity) -> bool:
        """
        Determines if the passed entity is currently considered enabled by the manager.

        :param item: Any entity
        :return: True if currently enabled, False if disabled
        """
        return cls._active_entity_manager.disable(item)

    @classmethod
    def is_enabled(cls, item: Entity) -> bool:
        return False

    @classmethod
    def _is_enabled_wrapper(cls, item: Entity) -> bool:
        return cls._active_entity_manager.is_enabled(item)

    @classmethod
    def _activate(cls) -> None:
        """
        Changes the methods to run their wrapper versions instead of the deferred
        versions.
        """
        cls.enable = cls._enable_wrapper
        cls.disable = cls._disable_wrapper
        cls.is_enabled = cls._is_enabled_wrapper

    @classmethod
    def set_entity_manager(cls, manager: AbstractEntityManager) -> None:
        cls._active_entity_manager = manager
        cls._activate()

    @staticmethod
    def get_entity_manager(**kwds) -> AbstractEntityManager:
        """
        Extracts an entity manager from keyword arguments.
        Gives the default entity manager if no entity manager is supplied.

        Used for getting an entity manager for a new game instance
        """
        if (entity_manager := kwds.get("entity_manager", None)) is None:
            manager_type = get_default_entity_manager_type()
            entity_manager = manager_type()
        return entity_manager


class AbstractEntityManager(ABC):

    def __new__(cls) -> Self:
        new_manager = super().__new__(cls)
        EntityManager.set_entity_manager(new_manager)
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
    def pre_update(self):
        """
        Runs the pre_update phase for active entities.
        """
        pass

    @abstractmethod
    def update(self):
        """
        Runs the update phase for active entities.
        """
        pass

    @abstractmethod
    def post_update(self):
        """
        Runs the post_update phase for active entities.
        """
        pass

    @abstractmethod
    def const_update(self):
        """
        Runs the const_update phase for active entities.
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


class DefaultEntityManager(AbstractEntityManager):

    def __init__(self) -> None:
        self.entities: WeakSet[Entity] = WeakSet()
        self._enabled_buffer: set[Entity] = set()
        self._disabled_buffer: set[Entity] = set()

        super().__init__()

    def enable(self, item: Entity) -> bool:
        if item in self._disabled_buffer:
            self._disabled_buffer.remove(item)
        else:
            self._enabled_buffer.add(item)
        return item not in self.entities

    def disable(self, item: Entity) -> bool:
        if item in self._enabled_buffer:
            self._enabled_buffer.remove(item)
        else:
            self._disabled_buffer.add(item)
        return item in self.entities

    def is_enabled(self, item: Entity) -> bool:
        return item in self._enabled_buffer or (
            item in self.entities and item not in self._disabled_buffer
        )

    def flush_buffer(self):
        self.entities |= self._enabled_buffer
        for entity in self._enabled_buffer:
            entity.OnEnable(entity)
            entity.on_enable()

        self.entities -= self._disabled_buffer

        for entity in self._disabled_buffer:
            entity.OnDisable(entity)
            entity.on_disable()

        self._enabled_buffer.clear()
        self._disabled_buffer.clear()

    def pre_update(self):
        for entity in self.entities:
            entity.pre_update()

    def update(self):
        for entity in self.entities:
            entity.update()

    def post_update(self):
        for entity in self.entities:
            entity.post_update()

    def const_update(self):
        for entity in self.entities:
            entity.const_update()

    def handle_event(self, event: pygame.Event):
        for entity in self.entities:
            entity.on_event(event)

    def get_number_entities(self) -> int:
        return len(self.entities)


_default_entity_manager_type = DefaultEntityManager


def get_default_entity_manager_type() -> type[AbstractEntityManager]:
    return _default_entity_manager_type


def set_default_entity_manager_type(manager_type: type[AbstractEntityManager]):
    global _default_entity_manager_type
    _default_entity_manager_type = manager_type
