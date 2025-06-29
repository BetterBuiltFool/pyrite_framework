# from collections.abc import Callable, Sequence
from contextlib import contextmanager
import pathlib
import sys
from weakref import WeakSet

# from typing import Any
import unittest


sys.path.append(str(pathlib.Path.cwd()))

from src.pyrite.core.entity_manager import DefaultEntityManager  # noqa:E402
from src.pyrite.types.entity import Entity  # noqa:E402


class MockEntity(Entity):

    def __init__(self, game_instance=None, enabled=True) -> None:
        pass


@contextmanager
def make_entity(*args, **kwds):
    yield MockEntity(*args, **kwds)


class TestDefaultEntityManager(unittest.TestCase):

    def setUp(self) -> None:
        self.entity_manager = DefaultEntityManager()

    def test_enable(self):
        # Ideal case

        with make_entity() as entity:
            self.assertNotIn(entity, self.entity_manager.entities)

            self.entity_manager.enable(entity)

            self.entity_manager.flush_buffer()

            self.assertIn(entity, self.entity_manager.entities)
            self.entity_manager.entities = WeakSet()

    def test_disable(self):
        entities = [MockEntity() for _ in range(5)]

        for entity in entities:
            self.entity_manager.enable(entity)

        self.entity_manager.flush_buffer()

        for entity in entities:
            self.assertIn(
                entity,
                self.entity_manager.entities,
            )

        disabled_entity = entities[2]  # Arbitrary index

        self.entity_manager.disable(disabled_entity)

        self.entity_manager.flush_buffer()

        for entity in entities:
            if entity is disabled_entity:
                continue
            self.assertIn(
                entity,
                self.entity_manager.entities,
            )
        self.assertNotIn(
            disabled_entity,
            self.entity_manager.entities,
        )

        # Try removing a renderable not in the collection
        self.entity_manager.disable(disabled_entity)


if __name__ == "__main__":

    unittest.main()
