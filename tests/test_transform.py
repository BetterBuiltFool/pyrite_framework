from __future__ import annotations

from typing import TYPE_CHECKING
import unittest

from pyglm import glm

from pyrite.transform import Transform, TransformComponent  # noqa:E402

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any

    from pygame.typing import Point

    from pyrite.types import TransformLike


class Empty:

    pass


class ObjectWithTransform:

    def __init__(self, transform: TransformLike) -> None:
        self._transform = transform

    @property
    def transform(self) -> TransformLike:
        return self._transform


def transform_from_euler(
    transformlike: tuple[Point, Point, Point | float],
) -> Transform:
    """
    A function for calling Transform.from_euler_rotation with a packed tuple.
    """
    return Transform.from_euler_rotation(
        transformlike[0], transformlike[1], transformlike[2]
    )


def transform_from_2d(transformlike: tuple[Point, float, Point | float]) -> Transform:
    return Transform.from_2d(transformlike[0], transformlike[1], transformlike[2])


class TestTransform(unittest.TestCase):

    def assertAlmostEqualVector3(
        self, first: glm.vec3, second: glm.vec3, places: int | None = None
    ) -> None:
        self.assertAlmostEqual(first.x, second.x, places)
        self.assertAlmostEqual(first.y, second.y, places)
        self.assertAlmostEqual(first.z, second.z, places)

    def test_inits(self) -> None:
        test_data = ((10, 10, 0), (0, 0, 0), (1, 1, 1))

        test_transform = Transform(
            glm.vec3(test_data[0]),
            glm.quat(glm.vec3(test_data[1])),
            glm.vec3(test_data[2]),
        )

        params: dict[str, tuple[TransformLike, Callable[[Any], Transform]]] = {
            "From Transform": (test_transform, Transform.from_transform),
            "From Attribute": (ObjectWithTransform(test_transform), Transform.new),
            "From Euler Rotation": (test_data, transform_from_euler),
            "From 2D": (((10, 10), 0, (1, 1)), transform_from_2d),
            "From Matrix": (test_transform.matrix, Transform.from_matrix),
        }

        for case, (transformlike, constructor) in params.items():
            with self.subTest(i=case):
                self.assertEqual(test_transform, constructor(transformlike))
                self.assertEqual(test_transform, Transform.new(transformlike))

    def test_generalize(self):

        world_transform = Transform.from_2d((10, 10), 90, (2, 2))

        local_transform = Transform.from_2d((5, 0), 0, (1, 1))

        modified = Transform.from_matrix(
            Transform.generalize(local_transform, world_transform)
        )

        expected = Transform.from_2d((10, 20), 90, (2, 2))

        self.assertAlmostEqualVector3(modified._position, expected._position, 5)
        self.assertEqual(modified.rotation, expected.rotation)
        self.assertEqual(modified.scale, expected.scale)

    def test_rmul(self):

        world_transform = Transform.from_2d((10, 10), 90, (2, 2))

        local_transform = Transform.from_2d((5, 0), 0, (1, 1))

        modified: Transform = Transform.from_matrix(world_transform * local_transform)

        expected = Transform.from_2d((10, 20), 90, (2, 2))

        self.assertAlmostEqualVector3(modified._position, expected._position, 5)
        self.assertEqual(modified.rotation, expected.rotation)
        self.assertEqual(modified.scale, expected.scale)

    def test_mul(self):

        empty = Empty()

        world_transform = TransformComponent(empty, (10, 10), 90, (2, 2))

        local_transform = Transform.from_2d((5, 0), 0, (1, 1))

        # TransformComponent has no __mul__, so Transform.__rmul__ takes over and
        # treats it like a transform.
        modified: Transform = Transform.from_matrix(world_transform * local_transform)

        expected = Transform.from_2d((10, 20), 90, (2, 2))

        self.assertEqual(modified.position, expected.position)
        self.assertEqual(modified.rotation, expected.rotation)
        self.assertEqual(modified.scale, expected.scale)

    def test_localize(self):

        root_transform = Transform.from_2d((10, 10), 90, (2, 2))
        branch_transform = Transform.from_2d((10, 20), 90, (2, 2))

        expected = Transform.from_2d((5, 0), 0, (1, 1))
        modified = Transform.from_matrix(
            Transform.localize(branch_transform, root_transform)
        )

        # Literally just the inverse of generalize()

        self.assertAlmostEqualVector3(modified._position, expected._position, 5)
        self.assertEqual(modified.rotation, expected.rotation)
        self.assertEqual(modified.scale, expected.scale)


if __name__ == "__main__":

    unittest.main()
