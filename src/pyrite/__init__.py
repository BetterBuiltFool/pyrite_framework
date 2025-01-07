import pygame

from ._data_classes.display_settings import DisplaySettings
from ._data_classes.game_data import GameData  # noqa:F401
from ._data_classes.timing_settings import TimingSettings  # noqa:F401
from .game import Game, AsyncGame  # noqa:F401
from .types.entity import Entity  # noqa:F401
from .types.renderable import Renderable  # noqa:F401

DEFAULT_WINDOWED: DisplaySettings = DisplaySettings()
"""
Basic windowed display, 800x600
"""
DEFAULT_FULLSCREEN: DisplaySettings = DisplaySettings(
    resolution=(0, 0), flags=pygame.FULLSCREEN
)
"""
Fullscreen view, native resolution.
Actual resolution supplied by pygame.
"""
