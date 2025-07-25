from __future__ import annotations
import unittest
from weakref import WeakKeyDictionary

from pyrite.component import Component


class ComponentA(Component):

    def foo(self):
        pass


class ComponentB(Component):

    def bar(self):
        pass


class ComponentC(Component):
    component_data: dict[Component, str] = {}

    def __init__(self, owner, data: str = "") -> None:
        super().__init__(owner)
        # Super simple test data
        self.component_data.update({self: data})

    @property
    def data(self) -> str:
        return self.component_data[self]

    @data.setter
    def data(self, value: str):
        self.component_data.update({self: value})

    @classmethod
    def _purge_component(cls, component: Component):
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
        component4 = ComponentC.get(self.object4)
        assert component4
        component4.data = "foo"
        self.object5 = TestOwner(True, True, False)  # A, B
        self.object6 = TestOwner(True, False, True)  # A, C
        component6 = ComponentC.get(self.object6)
        assert component6
        component6.data = "bar"
        self.object7 = TestOwner(False, True, True)  # B, C
        component7 = ComponentC.get(self.object7)
        assert component7
        component7.data = "baz"
        self.object8 = TestOwner(True, True, True)  # A, B, C
        component8 = ComponentC.get(self.object8)
        assert component8
        component8.data = "qux"

    def tearDown(self) -> None:
        ComponentA.instances = WeakKeyDictionary()
        ComponentB.instances = WeakKeyDictionary()
        ComponentC.instances = WeakKeyDictionary()
        ComponentC.component_data = {}

    def test_get(self):
        object2_component_a = ComponentA.get(self.object2)

        self.assertIsNotNone(object2_component_a)

        object1_component_a = ComponentA.get(self.object1)  # No such thing

        self.assertIsNone(object1_component_a)

    def test_intersect(self):
        shared_keys = ComponentA.intersect(ComponentB)
        goal_keys = {self.object5, self.object8}
        self.assertSetEqual(shared_keys, goal_keys)

        shared_keys = ComponentA.intersect(ComponentB, ComponentC)
        goal_keys = {self.object8}
        self.assertSetEqual(shared_keys, goal_keys)

        shared_keys = ComponentA.intersect()
        goal_keys = {self.object2, self.object5, self.object6, self.object8}
        self.assertSetEqual(shared_keys, goal_keys)

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
