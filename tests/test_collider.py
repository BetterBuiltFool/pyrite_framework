from __future__ import annotations
import math
import pathlib
import sys
import unittest

from pygame import Vector2, Rect

sys.path.append(str(pathlib.Path.cwd()))
from src.pyrite.shapes import Ellipse, Polygon, Stadium  # noqa:E402
from src.pyrite.collider.collider_system import ColliderSystem  # noqa:E402
from src.pyrite.collider.collider_component import ColliderComponent  # noqa:E402
from src.pyrite.collider import GJKFunctions  # noqa:E402
from src.pyrite.transform import Transform, TransformComponent  # noqa:E402


class TestOwner:

    pass


class TestColliderComponent(unittest.TestCase):

    def setUp(self):
        self.circle1 = Ellipse(5)
        self.circle2 = Ellipse(4)
        self.transform1 = Transform((1, 2))
        self.transform2 = Transform((5, 5))

    def test_gjk_support(self):

        # Cardinal direction, no rotation
        direction = Vector2(1, 0)

        result = self.circle1.get_furthest_vertex(direction, self.transform1)
        self.assertEqual(result, Vector2(6, 2))

        result = self.circle2.get_furthest_vertex(direction, self.transform2)
        self.assertEqual(result, Vector2(9, 5))

        # Orthoginal from past, no rotation
        direction = Vector2(0, 1)

        result = self.circle1.get_furthest_vertex(direction, self.transform1)
        self.assertEqual(result, Vector2(1, 7))

        result = self.circle2.get_furthest_vertex(direction, self.transform2)
        self.assertEqual(result, Vector2(5, 9))

        # Rotated direction vector, no transform rotation
        direction = Vector2(1, 0).rotate(45)

        result = self.circle1.get_furthest_vertex(direction, self.transform1)
        angle = math.cos(math.radians(45))
        expected = Vector2(
            (angle * 5) + self.transform1.position.x,
            (angle * 5) + self.transform1.position.y,
        )
        self.assertAlmostEqual(result.x, expected.x)
        self.assertAlmostEqual(result.y, expected.y)

        # Cardinal direction, rotation of transform
        # Ellipse is circular, so rotation of ellipse doesn't matter
        transform3 = Transform((1, 2), -45)
        direction = Vector2(1, 0)

        result = self.circle1.get_furthest_vertex(direction, transform3)
        angle = math.cos(math.radians(45))
        expected = Vector2(6, 2)
        self.assertEqual(result, expected)


class TestGJKFunctions(unittest.TestCase):

    def setUp(self) -> None:
        vertices = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        self.collider1 = Ellipse(5)
        self.collider2 = Ellipse(4)
        self.collider3 = Polygon([Vector2(*point) for point in vertices])
        self.collider4 = Stadium(1, 2)

    def test_support_function(self):
        direction = Vector2(1, 0)

        transform1 = Transform((5, 5))
        transform2 = Transform((-4, -4))
        transform3 = Transform((0, 0), 45)
        transform4 = Transform((5, 0), 90)

        sp1, *_ = GJKFunctions.support_function(
            direction, (self.collider1, transform1), (self.collider2, transform2)
        )

        self.assertEqual(sp1, Vector2(18, 9))

        sp2, *_ = GJKFunctions.support_function(
            direction, (self.collider1, transform1), (self.collider3, transform3)
        )

        expected = Vector2(10 + math.sqrt(2), 5)

        self.assertAlmostEqual(sp2.x, expected.x)
        self.assertAlmostEqual(sp2.y, expected.y)

        sp3, *_ = GJKFunctions.support_function(
            direction, (self.collider4, transform4), (self.collider2, transform2)
        )

        expected = Vector2(15, 4)

        self.assertEqual(sp3, expected)

    def test_normal(self):
        point_a = Vector2(-3, -4)
        point_b = Vector2(3, -2)
        normal = GJKFunctions.get_normal(point_a, point_b)
        edge = point_a - point_b

        self.assertEqual(edge, Vector2(-6, -2))

        self.assertEqual(normal, Vector2(-edge.y, edge.x))

    def test_check_region(self):

        region1 = [Vector2(1, 1), Vector2(-1, 1), Vector2(0, -1)]

        self.assertTrue(GJKFunctions.check_region(region1))

        region2 = [Vector2(1, 1), Vector2(-1, 1), Vector2(0, 2)]

        self.assertFalse(GJKFunctions.check_region(region2))

        # Same triangle as 1, opposing chirality

        region3 = [Vector2(-1, 1), Vector2(1, 1), Vector2(0, -1)]

        self.assertTrue(GJKFunctions.check_region(region3))

        # Needs addt'l edge cases
        # Literal origin on edge, vertex on origin

        # Origin on vertex
        region4 = [Vector2(1, 1), Vector2(-1, 1), Vector2(0, 0)]

        self.assertFalse(GJKFunctions.check_region(region4))

        # Origin on edge
        region5 = [Vector2(-1, 0), Vector2(1, 0), Vector2(0, 1)]

        self.assertTrue(GJKFunctions.check_region(region5))

    def test_collide(self):
        collider_a = Ellipse(5)
        collider_b = Ellipse(4)

        transform_a = Transform((5, 5))
        transform_b = Transform((-4, -4))

        # Obviously no overlap
        self.assertFalse(
            GJKFunctions.collide(collider_a, collider_b, transform_a, transform_b)
        )

        transform_c = Transform((0, 0))

        # This SHOULD overlap
        self.assertTrue(
            GJKFunctions.collide(collider_a, collider_b, transform_a, transform_c)
        )


class TestColliderSystem(unittest.TestCase):

    def setUp(self):
        self.object1 = TestOwner()
        self.object2 = TestOwner()

        TransformComponent(self.object1, (0, 0), 0, (1, 1))
        TransformComponent(self.object2, (4, 4), 0, (1, 1))

        collider1 = Ellipse(4)
        collider2 = Ellipse(4)

        ColliderComponent(self.object1, collider1, Transform(), 1, 1)
        ColliderComponent(self.object2, collider2, Transform(), 1, 1)

        ColliderSystem._set_collider_functions(GJKFunctions)

    def test_get_aabbs(self):

        aabbs = ColliderSystem.get_aabbs([self.object1, self.object2])

        expected = {
            self.object1: [Rect(-4, -4, 8, 8)],
            self.object2: [Rect(0, 0, 8, 8)],
        }

        self.assertEqual(aabbs, expected)

        self.assertTrue(aabbs[self.object1][0].colliderect(aabbs[self.object2][0]))

    def test_collide_between(self):
        component_a = ColliderComponent.get(self.object1)
        component_b = ColliderComponent.get(self.object2)

        self.assertTrue(ColliderSystem.collide_between(component_a, component_b))

    def test_get_first_pass_collisions(self):
        component_a = ColliderComponent.get(self.object1)
        component_b = ColliderComponent.get(self.object2)

        expected = {component_a: [component_b]}

        result = ColliderSystem.get_first_pass_collisions([self.object1, self.object2])

        self.assertEqual(result, expected)

        # Other cases:
        # - AABBS don't touch
        # - AABBS touch, even if colliders don't
        # - Results with mask mismatches

    def test_postupdate(self):
        component_a = ColliderComponent.get(self.object1)
        component_b = ColliderComponent.get(self.object2)

        collided_a = False
        collided_b = False

        @component_a.OnTouch.add_listener
        def _(this_collider: ColliderComponent, other_collider: ColliderComponent):
            nonlocal collided_a
            collided_a = True

        @component_b.OnTouch.add_listener
        def _(this_collider: ColliderComponent, other_collider: ColliderComponent):
            nonlocal collided_b
            collided_b = True

        test_system = ColliderSystem()

        test_system.post_update(0)

        self.assertTrue(collided_a)
        self.assertTrue(collided_b)

        # Other cases:
        # - No collision
        # - Mask mismatches
        # - Rotations


if __name__ == "__main__":

    unittest.main()
