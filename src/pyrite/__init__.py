import pygame

from .core.display_settings import DisplaySettings
from .core.game_data import GameData  # noqa:F401
from .core.rate_settings import RateSettings  # noqa:F401
from .core.renderer import get_render_manager, get_renderer  # noqa:F401
from .game import (  # noqa:F401
    Game,
    AsyncGame,
    get_system_manager,
    get_game_instance,
    get_entity_manager,
)

from .camera import Camera, ChaseCamera  # noqa:F401
from .types.entity import Entity  # noqa:F401
from .types.renderable import Renderable  # noqa:F401
from .enum import RenderLayers, AnchorPoint  # noqa: F401
from .sprite.sprite import Sprite  # noqa: F401
from .sprite.spritesheet import SpriteSheet, SpriteMap  # noqa: F401
from .types.system import System  # noqa: F401


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
