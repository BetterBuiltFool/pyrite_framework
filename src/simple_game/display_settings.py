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

    def create_window(self) -> pygame.Surface:
        """
        Updates the window based on the stored state.

        If vsync is enabled but not available, will default to disabled vsync.

        :return: A new surface representing the display.
        """
        try:
            window_surface = pygame.display.set_mode(
                self.resolution, self.flags, 0, self.display, self.vsync
            )
        except pygame.error:
            window_surface = pygame.display.set_mode(
                self.resolution, self.flags, 0, self.display
            )
            self.vsync = False
        return window_surface
