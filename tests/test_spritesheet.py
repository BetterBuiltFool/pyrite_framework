import pathlib
import sys
import unittest

import pygame


sys.path.append(str(pathlib.Path.cwd()))
from src.pyrite.sprite.spritesheet import (  # noqa:E402
    SimpleSpriteMap,
    SpriteSheet,
)

test_image = pygame.Surface((64, 64))
test_image.fill((0, 0, 0))
for i in range(8):
    for j in range(8):
        if i % 2 == j % 2:
            test_image.fill((255, 0, 255), (i, j, 8, 8))


class TestSpriteMap(SimpleSpriteMap):
    """
    Mockup sprite map that doesn't return the default rect on invalid key.
    """

    def get(self, key: tuple[int, int]) -> pygame.Rect:
        if key is None:
            return key
        row, column = key
        return self._map[row][column]


class TestSpriteSheet(unittest.TestCase):

    def setUp(self) -> None:
        sprite_map = TestSpriteMap(8, 8, (8, 8))
        self.spritesheet = SpriteSheet(test_image, sprite_map, start_state=(0, 0))

    def test_get_subsurface(self):
        key = (1, 1)

        subsurface = self.spritesheet._reference_sprite.subsurface(
            self.spritesheet.sprite_map.get(key)
        )

        self.assertEqual(
            # Since both surfaces are valid subsurfaces, their offsets should match.
            subsurface.get_offset(),
            self.spritesheet.get_subsurface(key).get_offset(),
        )

        invalid_key = None

        self.assertIsNone(
            # invalid key should cause None to be returned.
            self.spritesheet.get_subsurface(invalid_key),
        )


if __name__ == "__main__":

    unittest.main()
