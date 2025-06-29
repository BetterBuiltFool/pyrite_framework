from __future__ import annotations

from typing import TYPE_CHECKING

import cffi
import pygame

from .core.display_settings import DisplaySettings

if TYPE_CHECKING:
    pass

COMPONENT_TYPE: int = 2 ** (cffi.FFI().sizeof("int") * 8 - 1) - 1

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
