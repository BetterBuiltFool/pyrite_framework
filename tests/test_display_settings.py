import pathlib
import sys
import unittest

import pygame


sys.path.append(str(pathlib.Path.cwd()))
from src.simple_game.display_settings import DisplaySettings  # noqa:E402


class TestDisplay(unittest.TestCase):

    def test_get_display_settings(self):
        # Ideal case (All settings, no extras)
        kwds = {
            "resolution": (400, 300),
            "flags": pygame.HWSURFACE,
            "display": 0,
            "vsync": 0,
        }

        test_settings = DisplaySettings.get_display_settings(**kwds)

        self.assertEqual(test_settings.resolution, (400, 300))
        self.assertTrue(test_settings.flags & pygame.HWSURFACE)
        self.assertEqual(test_settings.display, 0)
        self.assertEqual(test_settings.vsync, 0)

        # All settings, extras
        kwds = {
            "resolution": (400, 300),
            "flags": pygame.HWSURFACE,
            "display": 0,
            "vsync": 0,
            "foo": False,
        }

        test_settings = DisplaySettings.get_display_settings(**kwds)

        self.assertEqual(test_settings.resolution, (400, 300))
        self.assertTrue(test_settings.flags & pygame.HWSURFACE)
        self.assertEqual(test_settings.display, 0)
        self.assertEqual(test_settings.vsync, 0)

        # Missing settings, no extras
        kwds = {
            "flags": pygame.HWSURFACE,
            "display": 0,
            "vsync": 0,
        }

        test_settings = DisplaySettings.get_display_settings(**kwds)

        self.assertEqual(test_settings.resolution, (800, 600))
        self.assertTrue(test_settings.flags & pygame.HWSURFACE)
        self.assertEqual(test_settings.display, 0)
        self.assertEqual(test_settings.vsync, 0)

        # Missing settings, extras
        kwds = {"flags": pygame.HWSURFACE, "display": 0, "vsync": 0, "foo": False}

        test_settings = DisplaySettings.get_display_settings(**kwds)

        self.assertEqual(test_settings.resolution, (800, 600))
        self.assertTrue(test_settings.flags & pygame.HWSURFACE)
        self.assertEqual(test_settings.display, 0)
        self.assertEqual(test_settings.vsync, 0)

        # No settings, no extras
        kwds = {}

        test_settings = DisplaySettings.get_display_settings(**kwds)

        self.assertEqual(test_settings.resolution, (800, 600))
        self.assertEqual(test_settings.flags, 0)
        self.assertEqual(test_settings.display, 0)
        self.assertEqual(test_settings.vsync, 0)

        # No settings, extras
        kwds = {"foo": False}

        test_settings = DisplaySettings.get_display_settings(**kwds)

        self.assertEqual(test_settings.resolution, (800, 600))
        self.assertEqual(test_settings.flags, 0)
        self.assertEqual(test_settings.display, 0)
        self.assertEqual(test_settings.vsync, 0)


if __name__ == "__main__":

    unittest.main()
