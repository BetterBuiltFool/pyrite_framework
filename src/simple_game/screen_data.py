import pygame

import pygame.typing


class ResolutionData:

    def __init__(
        self,
        size: pygame.typing.Point = (800, 600),
        flags: int = 0,
        display: int = 0,
        vsync: int = 0,
        **kwds
    ) -> None:
        """
        Creates a ResolutionData object.

        :param size: A Point-like object representing the width and height of the
        window, defaults to (800, 600)
        :param flags: Bitmask of pygame display flags, defaults to 0 (default pygame
        flags)
        :param display: Index of display used for set_mode
        :param vsync: Flag for enabling vsync, defaults to 0 (off)
        :param fullscreen: Boolean to force fullscreen mode (keyword-only)
        """
        self.is_fullscreen = (flags & pygame.FULLSCREEN) or kwds.get(
            "fullscreen", False
        )
        """
        Flag indicating that the game is operating in fullscreen mode.
        """
        if self.is_fullscreen:
            # Ensure the fullscreen flag is included if the fullscreen parameter is.
            flags = flags | pygame.FULLSCREEN
        self.resolution = size
        """
        A Point-like object representing the width and height of the window.
        """
        self.flags = flags
        """
        Bitmask of pygame display flags
        """
        self.display = display
        """
        Index of display used for set_mode
        """
        self.vsync = vsync
        """
        Flag for enabling vsync.

        0 = Off

        1 = On

        -1 = Adaptive vsync (requires OpenGL flag)
        """

    def rescale_window(self) -> pygame.Surface:
        """
        Updates the window based on the stored state.

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
