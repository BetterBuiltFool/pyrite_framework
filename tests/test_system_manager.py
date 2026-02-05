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

    def __init__(self, enabled=True) -> None:
        super().__init__(enabled)


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


if __name__ == "__main__":

    unittest.main()
