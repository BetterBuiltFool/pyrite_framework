from __future__ import annotations

from dataclasses import dataclass

import pygame


@dataclass
class Metadata:
    """
    A collection of data about a game.
    """

    name: str = "Game"
    """
    The name of the game.
    """
    caption: str = None
    """
    Text displayed by the title bar. Defaults to the game's name.
    """
    icon: pygame.Surface | None = None
    """
    Icon displayed in the title bar. 'None' uses the default pygame icon. Changes will
    only go into effect when the window is recreated.
    """

    def __post_init__(self):
        if self.caption is None:
            self.caption = self.name

    @staticmethod
    def get_metadata(**kwds) -> Metadata:
        """
        Creates a Metadata object from external arguments.
        Used for generating metadata from arguments passed into Game init.
        """
        metadata: Metadata | None = kwds.get("metadata", None)
        if metadata is None:
            # If no metadata object is supplied, create one.
            keys: set = {"name", "caption", "icon"}
            params: dict = {key: kwds[key] for key in keys if key in kwds}
            metadata = Metadata(**params)
        return metadata
