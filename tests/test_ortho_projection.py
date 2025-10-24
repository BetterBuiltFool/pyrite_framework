from __future__ import annotations

import unittest
from typing import TYPE_CHECKING

from pygame import Vector3

from pyrite._camera.ortho_projection import OrthoProjection

if TYPE_CHECKING:
    # from pyrite._types.projection import Projection
    pass

CENTERED_100_SQUARE = OrthoProjection((-50, -50, 100, 100))
CORNER_100_SQUARE = OrthoProjection((0, 0, 100, 100))
CENTERED_200X100 = OrthoProjection((-100, -50, 200, 100))


class TestOrthoProjection(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def test_ndc_to_eye(self) -> None:

        params: dict[str, tuple[OrthoProjection, Vector3, Vector3]] = {
            "Base Case C100S": (
                CENTERED_100_SQUARE,
                Vector3(0, 0, 0),
                Vector3(0, 0, 0),
            ),
            "Top left corner C100S": (
                CENTERED_100_SQUARE,
                Vector3(-1, 1, 0),
                Vector3(-50, 50, 0),
            ),
            "Bottom Right corner C100S": (
                CENTERED_100_SQUARE,
                Vector3(1, -1, 0),
                Vector3(50, -50, 0),
            ),
            "3/4x 3/4y C100S": (
                CENTERED_100_SQUARE,
                Vector3(0.5, 0.5, 0),
                Vector3(25, 25, 0),
            ),
            "Base Case Cr100S": (
                CORNER_100_SQUARE,
                Vector3(0, 0, 0),
                Vector3(50, -50, 0),
            ),
            "Top left corner Cr100S": (
                CORNER_100_SQUARE,
                Vector3(-1, 1, 0),
                Vector3(0, 0, 0),
            ),
            "Bottom Right corner Cr100S": (
                CORNER_100_SQUARE,
                Vector3(1, -1, 0),
                Vector3(100, -100, 0),
            ),
            "3/4x 3/4y Cr100S": (
                CORNER_100_SQUARE,
                Vector3(0.5, 0.5, 0),
                Vector3(75, -25, 0),
            ),
            "Base Case C2x1": (CENTERED_200X100, Vector3(0, 0, 0), Vector3(0, 0, 0)),
            "Top left corner C2x1": (
                CENTERED_200X100,
                Vector3(-1, 1, 0),
                Vector3(-100, 50, 0),
            ),
            "Bottom Right corner C2x1": (
                CENTERED_200X100,
                Vector3(1, -1, 0),
                Vector3(100, -50, 0),
            ),
            "3/4x 3/4y C2x1": (
                CENTERED_200X100,
                Vector3(0.5, 0.5, 0),
                Vector3(50, 25, 0),
            ),
        }

        for case, (projection, ndc_coords, expected_coords) in params.items():
            with self.subTest(i=case):
                result = projection.ndc_to_eye(ndc_coords)

                self.assertEqual(result, expected_coords)

    def test_eye_to_ndc(self) -> None:

        params: dict[str, tuple[OrthoProjection, Vector3, Vector3]] = {
            "Base Case C100S": (
                CENTERED_100_SQUARE,
                Vector3(0, 0, 0),
                Vector3(0, 0, 0),
            ),
            "Top left corner C100S": (
                CENTERED_100_SQUARE,
                Vector3(-50, 50, 0),
                Vector3(-1, 1, 0),
            ),
            "Bottom Right corner C100S": (
                CENTERED_100_SQUARE,
                Vector3(50, -50, 0),
                Vector3(1, -1, 0),
            ),
            "3/4x 3/4y C100S": (
                CENTERED_100_SQUARE,
                Vector3(25, 25, 0),
                Vector3(0.5, 0.5, 0),
            ),
            "Base Case Cr100S": (
                CORNER_100_SQUARE,
                Vector3(50, -50, 0),
                Vector3(0, 0, 0),
            ),
            "Top left corner Cr100S": (
                CORNER_100_SQUARE,
                Vector3(0, 0, 0),
                Vector3(-1, 1, 0),
            ),
            "Bottom Right corner Cr100S": (
                CORNER_100_SQUARE,
                Vector3(100, -100, 0),
                Vector3(1, -1, 0),
            ),
            "3/4x 3/4y Cr100S": (
                CORNER_100_SQUARE,
                Vector3(75, -25, 0),
                Vector3(0.5, 0.5, 0),
            ),
            "Base Case C2x1": (CENTERED_200X100, Vector3(0, 0, 0), Vector3(0, 0, 0)),
            "Top left corner C2x1": (
                CENTERED_200X100,
                Vector3(-100, 50, 0),
                Vector3(-1, 1, 0),
            ),
            "Bottom Right corner C2x1": (
                CENTERED_200X100,
                Vector3(100, -50, 0),
                Vector3(1, -1, 0),
            ),
            "3/4x 3/4y C2x1": (
                CENTERED_200X100,
                Vector3(50, 25, 0),
                Vector3(0.5, 0.5, 0),
            ),
        }

        for case, (projection, eye_coords, expected_coords) in params.items():
            with self.subTest(i=case):
                result = projection.eye_to_ndc(eye_coords)

                self.assertEqual(result, expected_coords)


if __name__ == "__main__":
    unittest.main()
