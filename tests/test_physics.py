from __future__ import annotations
import pathlib
import sys
import unittest

from pymunk import Circle, Shape

sys.path.append(str(pathlib.Path.cwd()))
from src.pyrite import Game  # noqa:E402
from src.pyrite.physics.physics_system import (  # noqa:E402
    get_collider_components,
    post_solve,
    separate,
)
from src.pyrite.transform import TransformComponent  # noqa:E402
from src.pyrite.physics.physics_service import PhysicsService  # noqa:E402
from src.pyrite.physics.rigidbody_component import RigidbodyComponent  # noqa:E402
from src.pyrite.physics.collider_component import ColliderComponent  # noqa:E402


class MockGame(Game):

    pass


class TestObject:

    pass


class MockArbiter:

    def __init__(self, shapes: tuple[Shape, Shape], is_first_contact: bool) -> None:
        self._shapes = shapes
        self._is_first_contact = is_first_contact

    @property
    def is_first_contact(self) -> bool:
        return self._is_first_contact

    @property
    def shapes(self) -> tuple[Shape, Shape]:
        return self._shapes


class TestPhysicsSystem(unittest.TestCase):

    def setUp(self) -> None:
        self.test_object_1 = TestObject()
        self.test_object_2 = TestObject()

        self.transform1 = TransformComponent(self.test_object_1)
        self.transform2 = TransformComponent(self.test_object_2)

        self.shape1 = Circle(None, radius=5)
        self.shape2 = Circle(None, radius=5)

        self.rb1 = RigidbodyComponent(self.test_object_1)
        self.rb2 = RigidbodyComponent(self.test_object_2)

        self.collider1: ColliderComponent = ColliderComponent(
            self.test_object_1, self.shape1
        )
        self.collider2: ColliderComponent = ColliderComponent(
            self.test_object_2, self.shape2
        )

    def test_get_collider_components(self):

        arbiter = MockArbiter((self.shape1, self.shape2), True)

        comp1, comp2 = get_collider_components(arbiter)

        self.assertIs(comp1, self.collider1)
        self.assertIs(comp2, self.collider2)

    def test_post_solve(self):

        arbiter = MockArbiter((self.shape1, self.shape2), True)

        test_var = False

        @self.collider1.OnTouch.add_listener
        def _(this_collider: ColliderComponent, other_collider: ColliderComponent):
            nonlocal test_var
            test_var = True

        post_solve(arbiter, PhysicsService.space, {})

        self.assertTrue(test_var)

    def test_separate(self):

        arbiter = MockArbiter((self.shape1, self.shape2), True)

        test_var = False

        @self.collider1.OnSeparate.add_listener
        def _(this_collider: ColliderComponent, other_collider: ColliderComponent):
            nonlocal test_var
            test_var = True

        separate(arbiter, PhysicsService.space, {})

        self.assertTrue(test_var)


if __name__ == "__main__":

    unittest.main()
