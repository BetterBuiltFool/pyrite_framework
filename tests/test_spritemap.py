import pathlib
import sys
import unittest

import pygame


sys.path.append(str(pathlib.Path.cwd()))
from src.pyrite.types.spritesheet import (  # noqa:E402
    RowColumnSpriteMap,
    StringSpriteMap,
)


class TestRowColumnSpriteMap(unittest.TestCase):

    def assertHasAttr(self, obj: object, attribute_name: str):
        self.assertTrue(
            hasattr(obj, attribute_name),
            msg=f"{obj=} lacks attribute: {attribute_name=}",
        )

    def test_init(self):
        # Create a sprite map with 5 rows (y), 10 columns (x), and a size of 100x100
        # pixels
        sprite_map = RowColumnSpriteMap(5, 10, (100, 100))
        self.assertHasAttr(sprite_map, "_map")
        self.assertTrue(len(sprite_map._map) == 5)
        self.assertTrue(len(sprite_map._map[0]) == 10)

        self.assertEqual(sprite_map.sprite_size, (100, 100))

    def test_get(self):
        sprite_map = RowColumnSpriteMap(5, 10, (100, 100))

        # Normal get
        rect = sprite_map.get((0, 0))

        self.assertIsNotNone(rect)
        self.assertEqual(rect, pygame.Rect(0, 0, 100, 100))

        # List instead of tuple
        rect = sprite_map.get([0, 0])

        self.assertIsNotNone(rect)
        self.assertEqual(rect, pygame.Rect(0, 0, 100, 100))

        # Default case
        rect = sprite_map.get(None)

        self.assertIsNotNone(rect)
        self.assertEqual(rect, pygame.Rect(0, 0, 100, 100))

        # Out of range (row)
        with self.assertRaises(IndexError):
            sprite_map.get((5, 0))

        # Out of range (col)
        with self.assertRaises(IndexError):
            sprite_map.get((0, 10))

        # Invalid key
        with self.assertRaises(TypeError):
            sprite_map.get(True)
            # Not subscriptable, expected tuple
        with self.assertRaises(TypeError):
            sprite_map.get("up")
            # Cannot use substrings for list indices
        with self.assertRaises(ValueError):
            sprite_map.get("five")
            # Cannot unpack string that long


if __name__ == "__main__":

    unittest.main()
