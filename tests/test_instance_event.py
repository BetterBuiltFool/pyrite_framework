import pathlib
import sys
import unittest


sys.path.append(str(pathlib.Path.cwd()))
from src.pyrite.types.instance_event import InstanceEvent  # noqa:E402


class OnTestEvent1(InstanceEvent):

    def __call__(self, param1: bool) -> None:
        return super().__call__(param1)


class OnTestEvent2(InstanceEvent):

    def __call__(self, param2: int) -> None:
        return super().__call__(param2)


class TestObject:

    def __init__(self) -> None:
        self.OnTestEvent1 = OnTestEvent1(self)
        self.OnTestEvent2 = OnTestEvent2(self)
        self.param1 = True
        self.param2 = 8


class TestInstanceEvent(unittest.TestCase):

    def setUp(self) -> None:
        self.test_object = TestObject()

    def test_register(self):

        def test_dummy():
            pass

        self.test_object.OnTestEvent1._register(test_dummy)

        self.assertIn(test_dummy, self.test_object.OnTestEvent1.listeners)

    def test_deregister(self):

        def test_dummy():
            pass

        self.test_object.OnTestEvent1._register(test_dummy)

        self.assertIn(test_dummy, self.test_object.OnTestEvent1.listeners)

        self.test_object.OnTestEvent1._deregister(test_dummy)

        self.assertNotIn(test_dummy, self.test_object.OnTestEvent1.listeners)

    def test_add_listener(self):

        @self.test_object.OnTestEvent1.add_listener
        def test_dummy(param1: bool):
            pass

        self.assertIn(test_dummy, self.test_object.OnTestEvent1.listeners)


if __name__ == "__main__":

    unittest.main()
