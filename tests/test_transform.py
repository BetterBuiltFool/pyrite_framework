from __future__ import annotations

from typing import TYPE_CHECKING
import unittest

from pyrite.transform import Transform, TransformComponent  # noqa:E402

if TYPE_CHECKING:
    from pyglm import glm


class Empty:

    pass


class TestTransform(unittest.TestCase):

    def assertAlmostEqualVector3(
        self, first: glm.vec3, second: glm.vec3, places: int | None = None
    ) -> None:
        self.assertAlmostEqual(first.x, second.x, places)
        self.assertAlmostEqual(first.y, second.y, places)
        self.assertAlmostEqual(first.z, second.z, places)

    def test_generalize(self):

        world_transform = Transform((10, 10), 90, (2, 2))

        local_transform = Transform((5, 0), 0, (1, 1))

        modified = Transform.generalize(local_transform, world_transform)

        expected = Transform((10, 20), 90, (2, 2))

        self.assertAlmostEqualVector3(modified._position, expected._position, 5)
        self.assertEqual(modified.rotation, expected.rotation)
        self.assertEqual(modified.scale, expected.scale)

    def test_rmul(self):

        world_transform = Transform((10, 10), 90, (2, 2))

        local_transform = Transform((5, 0), 0, (1, 1))

        modified: Transform = world_transform * local_transform

        expected = Transform((10, 20), 90, (2, 2))

        self.assertAlmostEqualVector3(modified._position, expected._position, 5)
        self.assertEqual(modified.rotation, expected.rotation)
        self.assertEqual(modified.scale, expected.scale)

    def test_mul(self):

        empty = Empty()

        world_transform = TransformComponent(empty, (10, 10), 90, (2, 2))

        local_transform = Transform((5, 0), 0, (1, 1))

        # TransformComponent has no __mul__, so Transform.__rmul__ takes over and
        # treats it like a transform.
        modified: Transform = world_transform * local_transform

        expected = Transform((10, 20), 90, (2, 2))

        self.assertEqual(modified.position, expected.position)
        self.assertEqual(modified.rotation, expected.rotation)
        self.assertEqual(modified.scale, expected.scale)

    def test_localize(self):

        root_transform = Transform((10, 10), 90, (2, 2))
        branch_transform = Transform((10, 20), 90, (2, 2))

        expected = Transform((5, 0), 0, (1, 1))
        modified = Transform.localize(branch_transform, root_transform)

        # Literally just the inverse of generalize()

        self.assertAlmostEqualVector3(modified._position, expected._position, 5)
        self.assertEqual(modified.rotation, expected.rotation)
        self.assertEqual(modified.scale, expected.scale)


if __name__ == "__main__":

    unittest.main()
