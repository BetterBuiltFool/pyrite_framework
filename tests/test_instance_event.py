import unittest
from weakref import WeakKeyDictionary

from pyrite.events import InstanceEvent
from pyrite._events.instance_event import SENTINEL
from pyrite.utils import threading


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
        self.test_object.OnTestEvent1.listeners = WeakKeyDictionary()
        self.test_object.OnTestEvent2.listeners = WeakKeyDictionary()

    def test_register(self):

        def test_dummy():
            pass

        self.test_object.OnTestEvent1._register(SENTINEL, test_dummy)

        callables = self.test_object.OnTestEvent1.listeners.get(SENTINEL)

        assert callables is not None

        self.assertIn(test_dummy, callables)

    def test_deregister(self):

        def test_dummy():
            pass

        self.test_object.OnTestEvent1._register(SENTINEL, test_dummy)

        callables = self.test_object.OnTestEvent1.listeners.get(SENTINEL)

        assert callables is not None

        self.assertIn(test_dummy, callables)

        self.test_object.OnTestEvent1._deregister(test_dummy)

        callables = self.test_object.OnTestEvent1.listeners.get(SENTINEL)

        assert callables is not None

        self.assertNotIn(test_dummy, callables)

    def test_add_listener(self):

        @self.test_object.OnTestEvent1.add_listener
        def test_dummy(param1: bool):
            pass

        callables = self.test_object.OnTestEvent1.listeners.get(SENTINEL)

        assert callables is not None

        self.assertIn(test_dummy, callables)

        event1 = self.test_object.OnTestEvent1

        class TestItem:
            def __init__(self) -> None:
                @event1.add_listener(self)
                def _(self):
                    pass

        test_item = TestItem()

        self.assertTrue(event1.listeners.get(test_item))

        class TestItem2:

            def test_method(self):
                pass

        test_item_2 = TestItem2()
        test_item_3 = TestItem2()

        event1.add_listener(test_item_2.test_method)

        callables = self.test_object.OnTestEvent1.listeners.get(SENTINEL)

        assert callables is not None

        self.assertIn(
            test_item_2.test_method,
            callables,
            # Bound methods go under SENTINEL
        )
        self.assertNotIn(
            test_item_3.test_method,
            callables,
        )

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

        # listeners on two separate events
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

    def test_multiple_listeners(self):

        self.value1 = None
        self.value2 = None

        @self.test_object.OnTestEvent1.add_listener
        def dummy1(param1):
            self.value1 = param1

        # listener of _same_ event
        @self.test_object.OnTestEvent1.add_listener
        def dummy2(param1):
            self.value2 = param1

        self.assertIsNone(self.value1)
        self.assertIsNone(self.value2)

        self.test_object.call_event_1()

        self.assertTrue(self.value1)
        self.assertTrue(self.value2)


if __name__ == "__main__":
    threading._active_threader = NonThreader()
    unittest.main()
