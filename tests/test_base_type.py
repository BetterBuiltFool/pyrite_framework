import pathlib
import sys
import unittest


sys.path.append(str(pathlib.Path.cwd()))
from src.pyrite.types import Container  # noqa:E402
from src.pyrite.types._base_type import _BaseType  # noqa:E402


class MockGame:

    def __init__(self) -> None:
        self.items = set()

    def enable(self, item: _BaseType) -> bool:
        new = item not in self.items
        self.items.add(item)
        return new

    def disable(self, item: _BaseType):
        new = item in self.items
        self.items.discard(item)
        return new


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

    def test_on_enable(self):
        class TestItem(_BaseType):
            def __init__(self, container: Container = None, enabled=True) -> None:
                super().__init__(container, enabled)
                self._is_enabled = enabled

            def on_enable(self):
                self._is_enabled = True

        test_item = TestItem(self.mock_game, False)

        self.assertNotIn(test_item, self.mock_game.items)
        self.assertFalse(test_item._is_enabled)

        test_item.enabled = True

        self.assertIn(test_item, self.mock_game.items)
        self.assertTrue(test_item._is_enabled)

    def test_on_preenable(self):
        class TestItem(_BaseType):
            def __init__(
                self,
                test_case: unittest.TestCase,
                container: Container = None,
                enabled=True,
            ) -> None:
                super().__init__(container, enabled)
                self.test_case = test_case

            def on_preenable(self):
                # Only true if item is not already enabled.
                self.test_case.assertNotIn(self, self.container.items)

        test_item = TestItem(self, self.mock_game, False)

        self.assertNotIn(test_item, self.mock_game.items)

        test_item.enabled = True

        self.assertIn(test_item, self.mock_game.items)

    def test_on_disable(self):
        class TestItem(_BaseType):
            def __init__(self, container: Container = None, enabled=True) -> None:
                super().__init__(container, enabled)
                self._is_enabled = enabled

            def on_disable(self):
                self._is_enabled = False

        test_item = TestItem(self.mock_game, True)

        self.assertIn(test_item, self.mock_game.items)
        self.assertTrue(test_item._is_enabled)

        test_item.enabled = False

        self.assertNotIn(test_item, self.mock_game.items)
        self.assertFalse(test_item._is_enabled)

    def test_on_predisable(self):
        class TestItem(_BaseType):
            def __init__(
                self,
                test_case: unittest.TestCase,
                container: Container = None,
                enabled=True,
            ) -> None:
                super().__init__(container, enabled)
                self.test_case = test_case

            def on_predisable(self):
                # Only true if item is not already disabled.
                self.test_case.assertIn(self, self.container.items)

        test_item = TestItem(self, self.mock_game, True)

        self.assertIn(test_item, self.mock_game.items)

        test_item.enabled = False

        self.assertNotIn(test_item, self.mock_game.items)


if __name__ == "__main__":

    unittest.main()
