import pathlib
import sys
import unittest

import pygame


sys.path.append(str(pathlib.Path.cwd()))
from src.pyrite.types._base_type import _BaseType  # noqa:E402
from src.pyrite.types.spritesheet import (  # noqa:E402
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


class MockGame:

    def __init__(self) -> None:
        self.items = set()

    def enable(self, item: _BaseType):
        self.items.add(item)

    def disable(self, item: _BaseType):
        self.items.discard(item)


class TestSpriteSheet(unittest.TestCase):

    def setUp(self) -> None:
        game = MockGame()
        sprite_map = TestSpriteMap(8, 8, (8, 8))
        self.spritesheet = SpriteSheet(
            test_image, sprite_map, start_state=(0, 0), container=game
        )

    def test_validate_state(self):

        # Case All params used, changing flip values

        self.assertEqual(
            ((0, 0), True, True), self.spritesheet._validate_state((0, 0), True, True)
        )

        # Case All params used, matching existing flip values

        self.assertEqual(
            ((0, 0), False, False),
            self.spritesheet._validate_state((0, 0), False, False),
        )

        # Case Default flip params

        self.assertEqual(
            ((0, 0), False, False),
            self.spritesheet._validate_state((0, 0), None, None),
        )

        # Case Default flip params with different current value

        self.spritesheet._flip_x = True

        self.assertEqual(
            ((0, 0), True, False),
            self.spritesheet._validate_state((0, 0), None, None),
        )

        self.spritesheet._flip_x = False

        # Case Default state key param

        self.assertEqual(
            ((0, 0), False, False),
            self.spritesheet._validate_state(None, False, False),
        )

        # Case match, no params used

        self.assertEqual(
            ((0, 0), False, False),
            self.spritesheet._validate_state(None, None, None),
        )

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

        self.assertIs(
            # invalid key should cause the current surface to be returned.
            self.spritesheet.surface,
            self.spritesheet.get_subsurface(invalid_key),
        )


if __name__ == "__main__":

    unittest.main()
