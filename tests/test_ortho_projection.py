from __future__ import annotations

import unittest
from typing import TYPE_CHECKING

from pygame import Vector2, Vector3

from pyrite._camera.ortho_projection import (
    OrthoProjection,
    DEFAULT_Z_NEAR,
    DEFAULT_Z_DEPTH,
)

if TYPE_CHECKING:
    from pygame.typing import Point

    type LocalCoords = Vector2
    type EyeCoords = Vector2
    type NDCCoords = Vector3
    type ZoomLevel = float

CENTERED_100_SQUARE = OrthoProjection(
    ((-50, -50, 100, 100), DEFAULT_Z_NEAR, DEFAULT_Z_DEPTH),
)
CORNER_100_SQUARE = OrthoProjection(
    ((0, 0, 100, 100), DEFAULT_Z_NEAR, DEFAULT_Z_DEPTH),
)
CENTERED_200X100 = OrthoProjection(
    ((-100, -50, 200, 100), DEFAULT_Z_NEAR, DEFAULT_Z_DEPTH),
)

CENTERED_800X600 = OrthoProjection(
    ((-400, -300, 800, 600), DEFAULT_Z_NEAR, DEFAULT_Z_DEPTH),
)
THREE_QUART_800X600 = OrthoProjection(
    ((-200, -150, 800, 600), DEFAULT_Z_NEAR, DEFAULT_Z_DEPTH),
)

ZERO_POINT = Vector2(0)
ZERO_3D = Vector3(0)


class TestOrthoProjection(unittest.TestCase):

    def assertAlmostEqualVector2(
        self, first: Point, second: Point, places: int | None = None
    ) -> None:

        self.assertAlmostEqual(first[0], second[0], places)
        self.assertAlmostEqual(first[1], second[1], places)

    def test_zoom(self) -> None:

        test_params: dict[str, tuple[OrthoProjection, ZoomLevel, OrthoProjection]] = {
            "Centered, zoom level 2": (
                CENTERED_100_SQUARE,
                2,
                OrthoProjection((-25, -25, -1, 50, 50, 2)),
            ),
            "Corner, zoom level 2": (
                CORNER_100_SQUARE,
                2,
                OrthoProjection((0, 0, -1, 50, 50, 2)),
            ),
            "Centered 200x100, zoom level 2": (
                CENTERED_200X100,
                2,
                OrthoProjection((-50, -25, -1, 100, 50, 2)),
            ),
        }

        for case, (projection, zoom_level, expected) in test_params.items():
            with self.subTest(i=case):
                zoom_proj = projection.zoom(zoom_level)

                self.assertEqual(zoom_proj, expected)


if __name__ == "__main__":
    unittest.main()
