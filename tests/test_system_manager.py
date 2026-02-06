from __future__ import annotations

from typing import cast, TYPE_CHECKING
import unittest

from pyrite.core.system_manager import DefaultSystemManager
from pyrite.systems import BaseSystem

if TYPE_CHECKING:
    pass


class MockSystem(BaseSystem):

    def __new__(cls, *args, **kwds) -> BaseSystem:
        return cast(BaseSystem, super().__new__(cls))

    def __init__(self, enabled=True, order_index: int = 0) -> None:
        super().__init__(enabled, order_index)


class TestSystemManager(unittest.TestCase):

    def setUp(self) -> None:
        self.system_manager = DefaultSystemManager()

    def flush(self):
        self.system_manager.prepare_systems()

    def test_enable(self) -> None:
        test_system = MockSystem(enabled=False)

        self.flush()

        self.assertNotIn(test_system, self.system_manager.active_systems)

        self.system_manager.enable(test_system)

        self.flush()

        self.assertIn(test_system, self.system_manager.active_systems)

        # No duplicates systems of the same type allowed, this should silently fail.
        second_system = MockSystem(enabled=False)

        self.flush()

        self.assertNotIn(second_system, self.system_manager.active_systems)

        self.system_manager.enable(second_system)

        self.flush()

        self.assertNotIn(second_system, self.system_manager.active_systems)

    def test_disable(self) -> None:
        test_system = MockSystem()

        self.flush()

        self.assertIn(test_system, self.system_manager.active_systems)

        self.system_manager.disable(test_system)

        self.flush()

        self.assertNotIn(test_system, self.system_manager.active_systems)

    def test_get_system(self) -> None:
        test_system = MockSystem()

        self.flush()

        result = self.system_manager.get_system(MockSystem)

        self.assertIs(result, test_system)

    def test_sort_systems(self) -> None:

        expected_priorities = [-2, -1, 0, 1, 2]

        test_systems: list[BaseSystem] = []

        for priority in expected_priorities:

            class TestSystem(MockSystem):
                def __init__(self, enabled=True, order_index: int = priority) -> None:
                    super().__init__(enabled, order_index)

            test_systems.append(TestSystem())

        expected_order = (
            test_systems[2],
            test_systems[3],
            test_systems[4],
            test_systems[1],
            test_systems[0],
        )

        ordered_systems = self.system_manager.sort_systems(test_systems)

        for system, expected in zip(ordered_systems, expected_order):
            self.assertIs(system, expected)


if __name__ == "__main__":

    unittest.main()
