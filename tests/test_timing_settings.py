from __future__ import annotations

import logging
import pathlib
import sys
import unittest

# import pygame


sys.path.append(str(pathlib.Path.cwd()))
import src.pyrite.timing_settings as timing_settings  # noqa:E402
from src.pyrite.timing_settings import TimingSettings  # noqa:E402

settings_logger = logging.getLogger(timing_settings.__name__)


class TestTimingSettingsModule(unittest.TestCase):

    def test_set_max_tick_rate(self):
        with self.assertLogs(settings_logger, logging.WARNING):
            timing_settings.set_max_tickrate(0)
        timing_settings.set_max_tickrate(120)


class TestTimingSettings(unittest.TestCase):

    def test_fps_cap(self):
        test_settings = TimingSettings(fps_cap=-1)
        self.assertEqual(test_settings._fps_cap, 0)

        with self.assertRaises(ValueError):
            test_settings.fps_cap = -1

    def test_tick_rate(self):
        test_settings = TimingSettings(tick_rate=-1)
        self.assertEqual(test_settings._tick_rate, 0)

        with self.assertLogs(settings_logger, logging.WARNING):
            test_settings.tick_rate = -1

        with self.assertLogs(settings_logger, logging.WARNING):
            test_settings.tick_rate = timing_settings.MAX_TICK_RATE_WARNING + 1

        with self.assertLogs(settings_logger, logging.INFO):
            test_settings.tick_rate = 0

        self.assertEqual(test_settings.fixed_timestep, -1)

        with self.assertLogs(settings_logger, logging.INFO):
            test_settings.tick_rate = 20

    def test_fixed_timestep(self):

        # Disabled tickrate
        test_settings = TimingSettings(tick_rate=0)
        self.assertEqual(test_settings._fixed_timestep, -1)

        # Default case
        test_settings = TimingSettings()
        self.assertEqual(test_settings._fixed_timestep, 0.05)

        # Set invalid timestep
        with self.assertRaises(ValueError):
            test_settings.fixed_timestep = 0

        # Recalculate tick rate
        test_settings.fixed_timestep = 0.1
        self.assertEqual(test_settings.tick_rate, 10)


if __name__ == "__main__":

    unittest.main()
