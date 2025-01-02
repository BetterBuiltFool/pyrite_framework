from __future__ import annotations

from dataclasses import dataclass
import typing

import pygame

import pygame.typing


@dataclass(frozen=True)
class DisplaySettings:
    """
    Object that contains data for generating a window for a game.

    :param resolution: A Point-like object representing the width and height of the
    window, defaults to (800, 600)
    :param flags: Bitmask of pygame display flags, defaults to 0 (default pygame
    flags)
    :param display: Index of display used for set_mode
    :param vsync: Flag for enabling vsync, defaults to 0 (off)
    """

    resolution: pygame.typing.Point = (800, 600)
    """
    A Point-like object representing the width and height of the window.
    """
    flags: int = 0
    """
    Bitmask of pygame display flags
    """
    display: int = 0
    """
    Index of display used for set_mode
    """
    vsync: int = 0
    """
    Flag for enabling vsync.

    0 = Off

    1 = On

    -1 = Adaptive vsync (requires OpenGL flag)
    """

    @property
    def is_fullscreen(self) -> bool:
        """
        Boolean indicating fullscreen status of the display.
        """
        return self.flags & pygame.FULLSCREEN

    @staticmethod
    def create_window(
        display_settings: DisplaySettings,
    ) -> tuple[pygame.Surface, DisplaySettings]:
        """
        Creates a window based on the given display settings. If vsync is enabled but
        not available, a new display settings is generated without vsync.

        :return: A new surface representing the display, and the display settings used
        by that surface.
        """
        try:
            window_surface = DisplaySettings._create_window(display_settings)
        except pygame.error:
            # Generate a new DisplaySettings without vsync enabled.
            new_settings = DisplaySettings(
                display_settings.resolution,
                display_settings.flags,
                display_settings.display,
                vsync=0,
            )
            display_settings = new_settings
            window_surface = DisplaySettings._create_window(display_settings)

        return window_surface, display_settings

    @staticmethod
    def _create_window(
        display_settings: DisplaySettings,
    ) -> pygame.Surface:
        return pygame.display.set_mode(
            display_settings.resolution,
            display_settings.flags,
            0,
            display_settings.display,
            display_settings.vsync,
        )

    @staticmethod
    def get_display_settings(**kwds) -> DisplaySettings:
        """
        Creates a DisplaySettings object from external arguments.
        Used for generating display setting from arguments passed into Game init.
        """
        display_settings: DisplaySettings | None = kwds.get("display_settings", None)
        if display_settings is None:
            # Create a new resolution data object, and check for and input settings.
            keys = {"resolution", "flags", "display", "vsync"}
            params: dict = {key: kwds[key] for key in keys if key in kwds}
            display_settings = DisplaySettings(**params)
        return typing.cast(DisplaySettings, display_settings)
