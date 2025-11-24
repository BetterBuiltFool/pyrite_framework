from __future__ import annotations

from typing import TYPE_CHECKING
import unittest

from pygame import Rect

from pyrite.cuboid import Cuboid

from pyrite.types import (
    has_cubelike_attribute,
    has_rect_like,
    is_sequence_based,
    is_number_sequence,
    is_3d_points,
)

if TYPE_CHECKING:
    from pygame.typing import RectLike

    from pyrite.types import CubeLike, CuboidTuple, _SequenceBased


class HasCuboidAttribute:

    def __init__(self) -> None:
        self.cuboid = Cuboid(0, 0, 0, 16, 16, 16)


class HasCuboidProperty:

    def __init__(self) -> None:
        self._cuboid = Cuboid(0, 0, 0, 16, 16, 16)

    @property
    def cuboid(self) -> CubeLike:
        return self._cuboid


class HasCuboidMethod:

    def __init__(self) -> None:
        self._cuboid = Cuboid(0, 0, 0, 16, 16, 16)

    def cuboid(self) -> CubeLike:
        return self._cuboid


class HasMetaCuboidMethod:

    def __init__(self) -> None:
        self._cuboid = HasCuboidMethod()

    def cuboid(self) -> CubeLike:
        return self._cuboid


class TestCuboid(unittest.TestCase):

    def setUp(self) -> None:
        self.basic_params: CuboidTuple = (0, 0, 0, 16, 16, 16)
        self.rect_params: RectLike = (
            self.basic_params[0],  # left
            self.basic_params[1],  # top
            self.basic_params[3],  # width
            self.basic_params[4],  # height
        )

    def test_has_cubelike_attribute(self) -> None:

        params: dict[str, tuple[CubeLike, bool]] = {
            "From RectLike+Point": ((self.rect_params, (0, 16)), False),
            "From RectLike+float+float": ((self.rect_params, 0, 16), False),
            "From Rect+Point": ((Rect(self.rect_params), (0, 16)), False),
            "From Attribute": (HasCuboidAttribute(), True),
            "From Property": (HasCuboidProperty(), True),
            "From Method": (HasCuboidMethod(), True),
            "From metamethod": (HasMetaCuboidMethod(), True),
        }

        for case, (cube_like, expected) in params.items():
            with self.subTest(i=case):
                result = has_cubelike_attribute(cube_like)

                self.assertEqual(result, expected)

    def test_is_sequence_based(self) -> None:

        params: dict[str, tuple[CubeLike, bool]] = {
            "From floats": (self.basic_params, True),
            "From RectLike+Point": ((self.rect_params, (0, 16)), True),
            "From RectLike+float+float": ((self.rect_params, 0, 16), True),
            "From Rect+Point": ((Rect(self.rect_params), (0, 16)), True),
            "From 3D Points": (((0, 0, 0), (16, 16, 16)), True),
            "From Attribute": (HasCuboidAttribute(), False),
            "From Property": (HasCuboidProperty(), False),
            "From Method": (HasCuboidMethod(), False),
            "From metamethod": (HasMetaCuboidMethod(), False),
        }

        for case, (cube_like, expected) in params.items():
            with self.subTest(i=case):
                result = is_sequence_based(cube_like)

                self.assertEqual(result, expected)

    def test_is_number_sequence(self) -> None:

        params: dict[str, tuple[_SequenceBased, bool]] = {
            "From floats": (self.basic_params, True),
            "From RectLike+Point": ((self.rect_params, (0, 16)), False),
            "From RectLike+float+float": ((self.rect_params, 0, 16), False),
            "From Rect+Point": ((Rect(self.rect_params), (0, 16)), False),
            "From 3D Points": (((0, 0, 0), (16, 16, 16)), False),
        }

        for case, (cube_like, expected) in params.items():
            with self.subTest(i=case):
                result = is_number_sequence(cube_like)

                self.assertEqual(result, expected)

    def test_is_3d_points(self) -> None:

        params: dict[str, tuple[_SequenceBased, bool]] = {
            "From floats": (self.basic_params, False),
            "From RectLike+Point": ((self.rect_params, (0, 16)), False),
            "From RectLike+float+float": ((self.rect_params, 0, 16), False),
            "From Rect+Point": ((Rect(self.rect_params), (0, 16)), False),
            "From 3D Points": (((0, 0, 0), (16, 16, 16)), True),
        }

        for case, (cube_like, expected) in params.items():
            with self.subTest(i=case):
                result = is_3d_points(cube_like)

                self.assertEqual(result, expected)

    def test_has_rect_like(self) -> None:

        params: dict[str, tuple[_SequenceBased, bool]] = {
            "From floats": (self.basic_params, False),
            "From RectLike+Point": ((self.rect_params, (0, 16)), True),
            "From RectLike+float+float": ((self.rect_params, 0, 16), True),
            "From Rect+Point": ((Rect(self.rect_params), (0, 16)), True),
            "From 3D Points": (((0, 0, 0), (16, 16, 16)), False),
        }

        for case, (cube_like, expected) in params.items():
            with self.subTest(i=case):
                result = has_rect_like(cube_like)

                self.assertEqual(result, expected)

    def test_init(self) -> None:

        # Our 'expected value' is also a test of the 6 floats init.
        basic_cuboid = Cuboid(*self.basic_params)

        # Params that _should_ work
        params: dict[str, CubeLike] = {
            "From Cuboid": basic_cuboid,
            "From RectLike+Point": (self.rect_params, (0, 16)),
            "From RectLike+float+float": (self.rect_params, 0, 16),
            "From Rect+Point": (Rect(self.rect_params), (0, 16)),
            "From 3D Points": ((0, 0, 0), (16, 16, 16)),
            "From Attribute": HasCuboidAttribute(),
            "From Property": HasCuboidProperty(),
            "From Method": HasCuboidMethod(),
            "From metamethod": HasMetaCuboidMethod(),
        }

        for case, cube_like in params.items():
            with self.subTest(i=case):
                cuboid = Cuboid(cube_like)

                self.assertEqual(cuboid, basic_cuboid)

        # Params expected to raise an exception
        bad_params: dict[str, CubeLike] = {
            "Bad Rectlike": ((0, 0, 16), 0, 16),
            "Missing Point": (self.rect_params,),  # type:ignore
            "Too Many Arguments": (self.rect_params, 0, 0, 0),  # type:ignore
        }

        for case, cube_like in bad_params.items():
            with self.subTest(i=case):
                with self.assertRaises(TypeError):
                    cuboid = Cuboid(cube_like)


if __name__ == "__main__":
    unittest.main()
