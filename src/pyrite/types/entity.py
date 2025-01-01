from ._base_type import _BaseType

import pygame


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
