from abc import abstractmethod, ABC

from ._base_type import _BaseType

import pygame


class Renderable(_BaseType, ABC):

    @abstractmethod
    def render(self, delta_time: float) -> tuple[pygame.Surface, pygame.Rect]:
        pass


class UIElement(_BaseType, ABC):

    @abstractmethod
    def render_ui(self, delta_time: float) -> tuple[pygame.Surface, pygame.Rect]:
        pass
