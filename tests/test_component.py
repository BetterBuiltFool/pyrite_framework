from __future__ import annotations
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
    component_data: dict[ComponentC, str] = {}

    def __init__(self, data: str = "") -> None:
        # Super simple test data
        self.component_data.update({self: data})

    @property
    def data(self) -> str:
        return self.component_data.get(self)

    @data.setter
    def data(self, value: str):
        self.component_data.update({self: value})

    @classmethod
    def _purge_component(cls, component: ComponentC):
        # This will raise without a valid component
        cls.component_data.pop(component)


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
        ComponentC.get(self.object4).data = "foo"
        self.object5 = TestOwner(True, True, False)  # A, B
        self.object6 = TestOwner(True, False, True)  # A, C
        ComponentC.get(self.object6).data = "bar"
        self.object7 = TestOwner(False, True, True)  # B, C
        ComponentC.get(self.object7).data = "baz"
        self.object8 = TestOwner(True, True, True)  # A, B, C
        ComponentC.get(self.object8).data = "qux"

    def tearDown(self) -> None:
        ComponentC.component_data = {}

    def test_intersect(self):
        shared_keys = ComponentA.intersect(ComponentB)
        self.assertSetEqual(shared_keys, {self.object5, self.object8})

        shared_keys = ComponentA.intersect(ComponentB, ComponentC)
        self.assertSetEqual(shared_keys, {self.object8})

        shared_keys = ComponentA.intersect()
        self.assertSetEqual(
            shared_keys, {self.object2, self.object5, self.object6, self.object8}
        )

    def test_remove_from(self):
        self.assertIn(self.object8, ComponentA.get_instances())

        ComponentA.remove_from(self.object8)

        self.assertNotIn(self.object8, ComponentA.get_instances())

        # See if we error removing an object not in A
        ComponentA.remove_from(self.object1)

    def test_remove_component(self):

        data = [data for data in ComponentC.component_data.values()]

        self.assertIn("qux", data)

        ComponentC.remove_from(self.object8)

        data = [data for data in ComponentC.component_data.values()]

        self.assertNotIn("qux", data)


if __name__ == "__main__":

    unittest.main()
