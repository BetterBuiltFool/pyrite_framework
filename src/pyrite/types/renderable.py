from abc import abstractmethod

from ._base_type import _BaseType

import pygame


class Renderable(_BaseType):

    @abstractmethod
    def render(self, delta_time: float) -> tuple[pygame.Surface, pygame.Rect]:
        pass


class UIElement(_BaseType):

    @abstractmethod
    def render_ui(self, delta_time: float) -> tuple[pygame.Surface, pygame.Rect]:
        pass
