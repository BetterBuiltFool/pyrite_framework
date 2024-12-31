from abc import ABC
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from .game import Game


class Updateable(ABC):

    def __init__(self) -> None:
        self.game: Game = None
        super().__init__()

    def pre_update(self, delta_time: float) -> None:
        pass

    def update(self, delta_time: float) -> None:
        pass

    def post_update(self, delta_time: float) -> None:
        pass

    def const_update(self, delta_time: float) -> None:
        pass


class Renderable(ABC):

    def render(self, delta_time: float) -> tuple[pygame.Surface, pygame.Rect]:
        pass

    def render_ui(self, delta_time: float) -> tuple[pygame.Surface, pygame.Rect]:
        pass
