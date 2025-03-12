import pathlib
import sys
import unittest

import pygame


sys.path.append(str(pathlib.Path.cwd()))
from src.pyrite.types._base_type import _BaseType  # noqa:E402
from src.pyrite.types.spritesheet import (  # noqa:E402
    SpriteSheet,
)

test_image = pygame.Surface((64, 64))
test_image.fill((0, 0, 0))
for i in range(8):
    for j in range(8):
        if i % 2 == j % 2:
            test_image.fill((255, 0, 255), (i, j, 8, 8))


class MockGame:

    def __init__(self) -> None:
        self.items = set()

    def enable(self, item: _BaseType):
        self.items.add(item)

    def disable(self, item: _BaseType):
        self.items.discard(item)


class TestSpriteSheet(unittest.TestCase):

    def setUp(self) -> None:
        self.spritesheet = SpriteSheet()
