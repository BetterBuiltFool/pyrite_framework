from abc import ABC

from .game import get_game_instance

import pygame


class _BaseType(ABC):

    def __init__(self) -> None:
        self._enabled: bool = True

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = value
        game_instance = get_game_instance()
        if value:
            game_instance.enable(self)
        else:
            game_instance.disable(self)


class Entity(_BaseType):

    def pre_update(self, delta_time: float) -> None:
        pass

    def update(self, delta_time: float) -> None:
        pass

    def post_update(self, delta_time: float) -> None:
        pass

    def const_update(self, delta_time: float) -> None:
        pass


class Renderable(_BaseType):

    def render(self, delta_time: float) -> tuple[pygame.Surface, pygame.Rect]:
        pass

    def render_ui(self, delta_time: float) -> tuple[pygame.Surface, pygame.Rect]:
        pass
