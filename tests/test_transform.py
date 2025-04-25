from __future__ import annotations
import pathlib
import sys
import unittest

sys.path.append(str(pathlib.Path.cwd()))
from src.pyrite.transform import Transform  # noqa:E402


class TestTransform(unittest.TestCase):

    def test_generalize(self):

        world_transform = Transform((10, 10), 90, (2, 2))

        local_transform = Transform((5, 0), 0, (1, 1))

        modified = local_transform.generalize(world_transform)

        expected = Transform((10, 0), 90, (2, 2))

        self.assertEqual(modified.position, expected.position)
        self.assertEqual(modified.rotation, expected.rotation)
        self.assertEqual(modified.scale, expected.scale)


if __name__ == "__main__":

    unittest.main()
