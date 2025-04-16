import pathlib
import sys
import unittest


sys.path.append(str(pathlib.Path.cwd()))
from src.pyrite.types import Component  # noqa:E402


class ComponentA(Component):

    def foo(self):
        pass


class ComponentB(Component):

    def bar(self):
        pass


class ComponentC(Component):
    pass


class TestOwner:

    def __init__(self, has_A: bool, has_B: bool, has_C: bool) -> None:
        self.components: list[Component] = []
        if has_A:
            self.components.append(ComponentA(self))
        if has_B:
            self.components.append(ComponentB(self))
        if has_C:
            self.components.append(ComponentC(self))


class TestComponent(unittest.TestCase):

    def setUp(self) -> None:
        self.object1 = TestOwner(False, False, False)  # None
        self.object2 = TestOwner(True, False, False)  # A
        self.object3 = TestOwner(False, True, False)  # B
        self.object4 = TestOwner(False, False, True)  # C
        self.object5 = TestOwner(True, True, False)  # A, B
        self.object6 = TestOwner(True, False, True)  # A, C
        self.object7 = TestOwner(False, True, True)  # B, C
        self.object8 = TestOwner(True, True, True)  # A, B, C

    def test_get_shared_keys(self):
        shared_keys = ComponentA.get_shared_keys(ComponentB)
        self.assertSetEqual(shared_keys, {self.object5, self.object8})

        shared_keys = ComponentA.get_shared_keys(ComponentB, ComponentC)
        self.assertSetEqual(shared_keys, {self.object8})


if __name__ == "__main__":

    unittest.main()
