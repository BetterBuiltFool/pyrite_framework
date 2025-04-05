import pygame

from .core.display_settings import DisplaySettings
from .core.game_data import GameData  # noqa:F401
from .core.rate_settings import RateSettings  # noqa:F401
from .game import Game, AsyncGame, get_game_instance  # noqa:F401
from .types.entity import Entity  # noqa:F401
from .types.renderable import Renderable  # noqa:F401
from .types.enums import RenderLayers, AnchorPoint  # noqa: F401


def get_system_manager():
    return get_game_instance().system_manager


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
