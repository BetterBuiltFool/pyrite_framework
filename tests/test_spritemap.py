from io import StringIO
import unittest

import pygame


from pyrite.sprite.spritesheet import (
    SimpleSpriteMap,
    DictSpriteMap,
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
        sprite_map = SimpleSpriteMap(5, 10, (100, 100))
        self.assertHasAttr(sprite_map, "_map")
        self.assertTrue(len(sprite_map._map) == 5)
        self.assertTrue(len(sprite_map._map[0]) == 10)

        self.assertEqual(sprite_map.sprite_size, (100, 100))

    def test_get(self):
        sprite_map = SimpleSpriteMap(5, 10, (100, 100))

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
            sprite_map.get(True)  # type:ignore[argument]
            # Not subscriptable, expected tuple
        with self.assertRaises(TypeError):
            sprite_map.get("up")  # type:ignore[argument]
            # Cannot use substrings for list indices
        with self.assertRaises(ValueError):
            sprite_map.get("five")  # type:ignore[argument]
            # Cannot unpack string that long


class TestStringSpriteMap(unittest.TestCase):

    def assertHasAttr(self, obj: object, attribute_name: str):
        self.assertTrue(
            hasattr(obj, attribute_name),
            msg=f"{obj=} lacks attribute: {attribute_name=}",
        )

    def test_init_from_dict(self):
        rects = {
            "one": pygame.Rect(0, 0, 100, 100),
            "two": pygame.Rect(100, 0, 100, 100),
            "three": pygame.Rect((100, 100, 50, 50)),
        }
        sprite_map = DictSpriteMap(rects)

        self.assertHasAttr(sprite_map, "_map")

        self.assertEqual(sprite_map._map["one"], rects["one"])
        self.assertEqual(sprite_map._map["two"], rects["two"])
        self.assertEqual(sprite_map._map["three"], rects["three"])

    def test_init_from_file(self):
        rects = {
            "one": pygame.Rect(0, 0, 100, 100),
            "two": pygame.Rect(100, 0, 100, 100),
            "three": pygame.Rect((100, 100, 50, 50)),
        }
        file = StringIO("one = 0 0 100 100\ntwo = 100 0 100 100\nthree = 100 100 50 50")
        sprite_map = DictSpriteMap.from_file(file)

        self.assertHasAttr(sprite_map, "_map")

        self.assertEqual(sprite_map._map["one"], rects["one"])
        self.assertEqual(sprite_map._map["two"], rects["two"])
        self.assertEqual(sprite_map._map["three"], rects["three"])

    def test_get(self):
        rects = {
            "one": pygame.Rect(0, 0, 100, 100),
            "two": pygame.Rect(100, 0, 100, 100),
            "three": pygame.Rect((100, 100, 50, 50)),
        }
        sprite_map = DictSpriteMap(rects)

        # Normal Case

        rect = sprite_map.get("one")

        self.assertEqual(rect, rects["one"])

        # Bad key

        with self.assertRaises(KeyError):

            sprite_map.get("Caboose")


if __name__ == "__main__":

    unittest.main()
