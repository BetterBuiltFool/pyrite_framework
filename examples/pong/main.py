"""
Pong is a very basic game, and thus makes for a good introduction to the basic usage of
Pyrite.

This example makes use of no image assets.
"""

from __future__ import annotations

import pyrite
from pyrite.types import Container
from pyrite.types.enums import Layer

import pygame


class Paddle(pyrite.Entity, pyrite.Renderable):

    def __init__(
        self,
        container: Container = None,
        enabled=True,
        layer: Layer = None,
        draw_index=0,
        start_postion: pygame.typing.Point = (0, 0),
    ) -> None:
        super().__init__(container, enabled, layer, draw_index)

        self.position = pygame.Vector2(start_postion)
        self.size = (10, 32)

        self.surface = pygame.Surface(self.size)
        self.surface.fill(pygame.Color("white"))

    def update(self, delta_time: float):
        pass

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.position, self.size)

    def render(self, delta_time: float) -> pygame.Surface:
        return self.surface


if __name__ == "__main__":
    with pyrite.Game(resolution=(800, 500)) as pong_game:
        pong_game.game_data.title = "Example Pong"
