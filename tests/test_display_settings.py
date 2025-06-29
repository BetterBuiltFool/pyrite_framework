from __future__ import annotations

import pathlib
import sys
from typing import cast, Self
import unittest

import pygame


sys.path.append(str(pathlib.Path.cwd()))
from src.pyrite.core.display_settings import DisplaySettings  # noqa:E402


class MockSurface:
    """
    A simple singleton object to fill in for a surface.
    """

    _instance: Self | None = None

    def __new__(cls, *args, **kwds) -> pygame.Surface:
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwds)
        # We need to claim we're returning a surface to make static checkers happy.
        return cast(pygame.Surface, cls._instance)


class TestDisplay(unittest.TestCase):

    def test_create_window(self):

        vsync_allowed: bool = True

        def mock_create_window(
            display_settings: DisplaySettings,
        ) -> pygame.Surface:
            if not display_settings.vsync == 1 or (
                vsync_allowed and display_settings.vsync == 1
            ):
                surf = MockSurface()
                return surf
            raise pygame.error()

        DisplaySettings._create_window = mock_create_window

        # default settings, vsync allowed (moot)

        test_settings = DisplaySettings()

        mocked_surf, result_settings = DisplaySettings.create_window(test_settings)

        self.assertEqual(mocked_surf, MockSurface())
        self.assertIs(test_settings, result_settings)

        # default settings, vsync disallowed

        test_settings = DisplaySettings()
        vsync_allowed = False

        mocked_surf, result_settings = DisplaySettings.create_window(test_settings)

        self.assertEqual(mocked_surf, MockSurface())
        self.assertIs(test_settings, result_settings)

        # vsync enabled, vsync allowed

        test_settings = DisplaySettings(vsync=1)
        vsync_allowed = True

        mocked_surf, result_settings = DisplaySettings.create_window(test_settings)

        self.assertEqual(mocked_surf, MockSurface())
        self.assertIs(test_settings, result_settings)

        # vsync enabled, vsync disallowed

        test_settings = DisplaySettings(vsync=1)
        vsync_allowed = False

        mocked_surf, result_settings = DisplaySettings.create_window(test_settings)

        self.assertEqual(mocked_surf, MockSurface())
        self.assertIsNot(test_settings, result_settings)

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
