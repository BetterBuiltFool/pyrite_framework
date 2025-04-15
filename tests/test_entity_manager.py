# from collections.abc import Callable, Sequence
from contextlib import contextmanager
import pathlib
import sys

# from typing import Any
import unittest

from pygame.rect import Rect as Rect
from pygame.surface import Surface as Surface
from pygame.typing import Point


sys.path.append(str(pathlib.Path.cwd()))

from src.pyrite.core.entity_manager import DefaultEntityManager  # noqa:E402
from src.pyrite.enum import Layer  # noqa:E402
from src.pyrite.types.entity import Entity  # noqa:E402
from src.pyrite.types.renderable import Renderable  # noqa:E402


class MockRenderable(Renderable):

    def __init__(
        self, game_instance=None, enabled=True, layer: Layer = None, draw_index=-1
    ) -> None:
        self._layer = layer
        self.draw_index = draw_index

    def render(self, delta_time: float) -> tuple[Surface, Point | Rect]:
        return super().render(delta_time)

    def get_rect(self) -> Rect:
        return super().get_rect()


class MockEntity(Entity):

    def __init__(self, game_instance=None, enabled=True) -> None:
        pass


@contextmanager
def make_renderable(*args, **kwds):
    yield MockRenderable(*args, **kwds)


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
            self.entity_manager.entities = set()

        # Non-entity
        with make_renderable() as renderable:
            self.assertNotIn(entity, self.entity_manager.entities)

            self.entity_manager.enable(renderable)

            self.entity_manager.flush_buffer()

            self.assertNotIn(renderable, self.entity_manager.entities)
            self.entity_manager.entities = set()

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

        # Try removing a mock renderable
        renderable = MockRenderable()

        self.entity_manager.disable(renderable)

        # Try removing a renderable not in the collection
        self.entity_manager.disable(disabled_entity)


if __name__ == "__main__":

    unittest.main()
