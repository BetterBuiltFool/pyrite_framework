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

    def test_enable(self):
        mock_game = MockGame()
        test_entities = [TestEntity(game_instance=mock_game) for _ in range(5)]

        for entity in test_entities:
            self.assertIn(entity, mock_game.items)

    def test_disable(self):
        mock_game = MockGame()
        test_entities = {TestEntity(game_instance=mock_game) for _ in range(5)}

        disabled_entities: set[TestEntity] = {
            entity for index, entity in enumerate(test_entities) if index % 2 == 0
        }
        enabled_entities = test_entities - disabled_entities

        for entity in enabled_entities:
            self.assertIn(entity, mock_game.items)

        for entity in disabled_entities:
            entity.enabled = False
            self.assertNotIn(entity, mock_game.items)


if __name__ == "__main__":

    unittest.main()
