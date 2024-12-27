from __future__ import annotations

from dataclasses import dataclass

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
    def is_fullscreen(self):
        return self.flags & pygame.FULLSCREEN

    @staticmethod
    def create_window(
        display_settings: DisplaySettings,
    ) -> tuple[pygame.Surface, DisplaySettings]:
        """
        Updates the window based on the stored state.

        If vsync is enabled but not available, will default to disabled vsync.

        :return: A new surface representing the display, and the display settings used
        by that surface.
        """
        try:
            window_surface = pygame.display.set_mode(
                display_settings.resolution,
                display_settings.flags,
                0,
                display_settings.display,
                display_settings.vsync,
            )
        except pygame.error:
            window_surface = pygame.display.set_mode(
                display_settings.resolution,
                display_settings.flags,
                0,
                display_settings.display,
            )
            # Generate a new DisplaySettings without vsync enabled.
            new_settings = DisplaySettings(
                display_settings.resolution,
                display_settings.flags,
                display_settings.display,
                vsync=False,
            )
            display_settings = new_settings

        return window_surface, display_settings
