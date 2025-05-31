from __future__ import annotations

import pathlib
import sys
from typing import TYPE_CHECKING
import unittest

from pygame import Rect

if TYPE_CHECKING:
    pass

sys.path.append(str(pathlib.Path.cwd()))
from src.pyrite.rendering.ortho_projection import OrthProjection  # noqa:E402


class TestOrthoProjection(unittest.TestCase):

    def setUp(self) -> None:
        projection_rect = Rect(0, 0, 800, 600)
        self.projection = OrthProjection(projection_rect)

    def test_clip_to_ndc(self):
        pass

    def test_ndc_to_clip(self):
        pass


if __name__ == "__main__":
    unittest.main()
