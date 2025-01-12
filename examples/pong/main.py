"""
Pong is a very basic game, and thus makes for a good introduction to the basic usage of
Pyrite.

This example makes use of no image assets.
"""

from __future__ import annotations

from typing import Protocol

import pyrite
from pyrite.types import Container
from pyrite.types.enums import Layer, RenderLayers

import pygame


class Paddle(pyrite.Entity, pyrite.Renderable):

    def __init__(
        self,
        container: Court = None,
        enabled=True,
        layer: Layer = None,
        draw_index=0,
        start_postion: pygame.typing.Point = (0, 0),
    ) -> None:
        super().__init__(container, enabled, layer, draw_index)

        self.container: Court = container
        self.position = pygame.Vector2(start_postion)
        self.size = pygame.Vector2(10, 64)

        self.max_speed = 256
        self.velocity = 0

        self.surface = pygame.Surface(self.size)
        self.surface.fill(pygame.Color("white"))

    def update(self, delta_time: float):
        self.position.y += self.velocity * delta_time
        self.position.y = max(
            0, min(self.position.y, (self.container.size.y - self.size.y))
        )

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.position, self.size)

    def render(self, delta_time: float) -> pygame.Surface:
        return self.surface


class PaddleController(Protocol):
    paddle: Paddle


class PlayerController(pyrite.Entity):

    def __init__(
        self,
        container: Container = None,
        enabled=True,
        paddle: Paddle = None,
        control_keys: tuple[int, int] = (0, 0),
    ) -> None:
        super().__init__(container, enabled)
        self.paddle = paddle
        self.up_key = control_keys[0]
        self.down_key = control_keys[1]

    def pre_update(self, delta_time: float) -> None:
        keys = pygame.key.get_pressed()
        y = 0
        if keys[self.up_key]:
            y -= 1
        if keys[self.down_key]:
            y += 1
        if self.paddle is not None:
            self.paddle.velocity = self.paddle.max_speed * y


class Net(pyrite.Renderable):

    def __init__(
        self,
        container: Container = None,
        enabled=True,
        draw_index=0,
        position: pygame.typing.Point = (0, 0),
    ) -> None:
        layer = RenderLayers.BACKGROUND
        super().__init__(container, enabled, layer, draw_index)
        self.position = pygame.Vector2(position)
        self.size = pygame.Vector2(10, 500)

        self.surface = pygame.Surface(self.size)

        for index in range(10):
            pygame.draw.rect(
                self.surface,
                pygame.Color("gray88"),
                pygame.Rect(0, 12 + index * 50, 10, 25),
            )

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.position, self.size)

    def render(self, delta_time: float):
        return self.surface


class Ball(pyrite.Entity, pyrite.Renderable):

    def __init__(
        self,
        container: Container = None,
        enabled=True,
        layer: Layer = None,
        draw_index=0,
        start_position: pygame.typing.Point = (0, 0),
    ) -> None:
        super().__init__(container, enabled, layer, draw_index)

        self.position = pygame.Vector2(start_position)
        self.size = pygame.Vector2(16, 16)

        self.surface = pygame.Surface(self.size)
        self.surface.fill(pygame.Color("white"))

    def update(self, delta_time: float) -> None:
        pass

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.position, self.size)

    def render(self, delta_time: float) -> pygame.Surface:
        return self.surface


class Court(pyrite.Entity):

    def __init__(
        self,
        game_instance: pyrite.Game = None,
        enabled=True,
        court_size: pygame.Vector2 = None,
    ) -> None:
        super().__init__(game_instance, enabled)

        if court_size is None:
            court_size = pygame.Vector2(game_instance.window.size)

        self.size = court_size

        self.p1_paddle = Paddle(self)
        self.p1_paddle.position = pygame.Vector2(
            10, (self.size.y / 2) - (self.p1_paddle.size.y / 2)
        )

        self.p2_paddle = Paddle(self)
        self.p2_paddle.position = pygame.Vector2(
            self.size.x - 20, (self.size.y / 2) - (self.p2_paddle.size.y / 2)
        )

        self.net = Net(self)
        self.net.position = pygame.Vector2((self.size.x / 2) - (self.net.size.x / 2), 0)

        self.player1_controller: PaddleController = PlayerController(
            self, paddle=self.p1_paddle, control_keys=(pygame.K_w, pygame.K_s)
        )

        self.player2_controller: PaddleController = PlayerController(
            self, paddle=self.p2_paddle, control_keys=(pygame.K_UP, pygame.K_DOWN)
        )

    def enable(self, item):
        self.container.enable(item)

    def disable(self, item):
        self.container.disable(item)


if __name__ == "__main__":
    with pyrite.Game(resolution=(800, 500)) as pong_game:
        pong_game.game_data.title = "Example Pong"
        court = Court(pong_game)
