import pathlib
import sys
import unittest


sys.path.append(str(pathlib.Path.cwd()))
from src.pyrite.types.instance_event import InstanceEvent  # noqa:E402
from src.pyrite.utils import threading  # noqa:E402


class NonThreader(threading.BaseThreader):
    """
    Special test threader that doesn't actually start threads, to make testing easier.
    """

    def start_thread(self, callable_, *args, **kwds) -> None:
        callable_(*args, **kwds)


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

    def call_event_1(self):
        self.OnTestEvent1(self.param1)

    def call_event_2(self):
        self.OnTestEvent2(self.param2)


class TestInstanceEvent(unittest.TestCase):

    def setUp(self) -> None:
        self.test_object = TestObject()

    def tearDown(self) -> None:
        self.test_object.OnTestEvent1.listeners = set()
        self.test_object.OnTestEvent2.listeners = set()

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

    def test_notify(self):

        self.value1 = None

        @self.test_object.OnTestEvent1.add_listener
        def test_dummy(param1: bool):
            self.value1 = param1

        self.assertIsNone(self.value1)

        self.test_object.OnTestEvent1._notify(True)

        self.assertTrue(self.value1)

    def test_call_(self):

        self.value1 = None
        self.value2 = None

        @self.test_object.OnTestEvent1.add_listener
        def test_dummy(param1: bool):
            self.value1 = param1

        @self.test_object.OnTestEvent2.add_listener
        def test_dummy2(param2: int):
            self.value2 = param2

        self.assertIsNone(self.value1)
        self.assertIsNone(self.value2)

        self.test_object.call_event_1()

        self.assertTrue(self.value1)
        self.assertIsNone(self.value2)

        self.test_object.call_event_2()

        self.value1 = None

        self.assertIsNone(self.value1)
        self.assertEqual(self.value2, 8)


if __name__ == "__main__":
    threading._active_threader = NonThreader()
    unittest.main()
