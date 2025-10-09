from __future__ import annotations

from typing import TYPE_CHECKING
import unittest


from pyrite._types.shape import Shape

from pyrite._physics.shapes import Circle, Polygon

if TYPE_CHECKING:
    from typing import Any


class TestShapes(unittest.TestCase):

    def setUp(self) -> None:
        self.circle1 = Circle(None, 10)
        self.circle2 = Circle(None, 20)
        self.circle3 = Circle(None, 30)
        self.box = Polygon.make_box(None, (10, 10))
        self.shapes: list[Shape[Any]] = [
            self.circle1,
            self.circle2,
            self.circle3,
            self.box,
        ]

    def tearDown(self) -> None:
        Shape._shapes.clear()

    def test_get_shape(self) -> None:
        self.assertEqual(len(Shape._shapes), len(self.shapes))

        for shape in self.shapes:
            self.assertIn(shape._shape, Shape._shapes)


if __name__ == "__main__":

    unittest.main()
