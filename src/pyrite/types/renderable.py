from ._base_type import _BaseType

import pygame


class Renderable(_BaseType):

    def render(self, delta_time: float) -> tuple[pygame.Surface, pygame.Rect]:
        pass

    def render_ui(self, delta_time: float) -> tuple[pygame.Surface, pygame.Rect]:
        pass
