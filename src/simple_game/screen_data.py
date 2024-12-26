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
        self.resolution = size
        self.flags = flags
        self.display = display
        self.vsync = vsync
        self.is_fullscreen = (self.flags & pygame.FULLSCREEN) or kwds.get(
            "fullscreen", False
        )
        pygame.display.set_mode()

    def rescale_window(self) -> pygame.Surface:
        return pygame.display.set_mode(
            self.resolution, self.flags, 0, self.display, self.vsync
        )
