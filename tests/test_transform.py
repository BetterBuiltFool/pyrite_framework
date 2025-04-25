from __future__ import annotations
import pathlib
import sys
import unittest

sys.path.append(str(pathlib.Path.cwd()))
from src.pyrite.transform import Transform, TransformComponent  # noqa:E402


class Empty:

    pass


class TestTransform(unittest.TestCase):

    def test_generalize(self):

        world_transform = Transform((10, 10), 90, (2, 2))

        local_transform = Transform((5, 0), 0, (1, 1))

        modified = local_transform.generalize(world_transform)

        expected = Transform((10, 0), 90, (2, 2))

        self.assertEqual(modified.position, expected.position)
        self.assertEqual(modified.rotation, expected.rotation)
        self.assertEqual(modified.scale, expected.scale)

    def test_rmul(self):

        world_transform = Transform((10, 10), 90, (2, 2))

        local_transform = Transform((5, 0), 0, (1, 1))

        modified: Transform = world_transform * local_transform

        expected = Transform((10, 0), 90, (2, 2))

        self.assertEqual(modified.position, expected.position)
        self.assertEqual(modified.rotation, expected.rotation)
        self.assertEqual(modified.scale, expected.scale)

    def test_mul(self):

        empty = Empty()

        world_transform = TransformComponent(empty, (10, 10), 90, (2, 2))

        local_transform = Transform((5, 0), 0, (1, 1))

        # TransformComponent has no __mul__, so Transform.__rmul__ takes over and
        # treats it like a transform.
        modified: Transform = world_transform * local_transform

        expected = Transform((10, 0), 90, (2, 2))

        self.assertEqual(modified.position, expected.position)
        self.assertEqual(modified.rotation, expected.rotation)
        self.assertEqual(modified.scale, expected.scale)

    def test_localize(self):

        root_transform = Transform((10, 10), 90, (2, 2))
        branch_transform = Transform((10, 0), 90, (2, 2))

        expected = Transform((5, 0), 0, (1, 1))
        modified = branch_transform.localize(root_transform)

        # Literally just the inverse of generalize()

        self.assertEqual(modified.position, expected.position)
        self.assertEqual(modified.rotation, expected.rotation)
        self.assertEqual(modified.scale, expected.scale)


if __name__ == "__main__":

    unittest.main()
