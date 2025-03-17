import pathlib
import sys
import unittest


sys.path.append(str(pathlib.Path.cwd()))
from src.pyrite.types._base_type import _BaseType  # noqa:E402


class MockGame:

    def __init__(self) -> None:
        self.items = set()

    def enable(self, item: _BaseType):
        self.items.add(item)

    def disable(self, item: _BaseType):
        self.items.discard(item)


class TestEntity(_BaseType):

    def __init__(self, game_instance=None, enabled=True) -> None:
        super().__init__(game_instance, enabled)


class Test_BaseType(unittest.TestCase):

    def setUp(self) -> None:
        self.mock_game = MockGame()
        self.test_entities = [
            TestEntity(game_instance=self.mock_game) for _ in range(5)
        ]

    def test_enable(self):

        for entity in self.test_entities:
            self.assertIn(entity, self.mock_game.items)

    def test_disable(self):

        test_entities = set(self.test_entities)
        disabled_entities: set[TestEntity] = {
            entity for index, entity in enumerate(self.test_entities) if index % 2 == 0
        }
        enabled_entities = test_entities - disabled_entities

        for entity in enabled_entities:
            self.assertIn(entity, self.mock_game.items)

        for entity in disabled_entities:
            entity.enabled = False
            self.assertNotIn(entity, self.mock_game.items)


if __name__ == "__main__":

    unittest.main()
