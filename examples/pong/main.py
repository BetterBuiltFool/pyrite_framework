"""
Pong is a very basic game, and thus makes for a good introduction to the basic usage of
Pyrite.

This example makes use of no image assets.

Sound effects courtesy of Kenney.nl, via opengameart.org
"""

from __future__ import annotations

import math
from pathlib import Path
import random
from typing import Protocol

import pyrite
from pyrite.types import Container
from pyrite.types.enums import Layer, RenderLayers

import pygame

pygame.init()


class Paddle(pyrite.Entity, pyrite.Renderable):
    hit_sounds: list[pygame.Sound] = [
        pygame.Sound(Path(f"examples/pong/assets/sounds/phaserUp{i+1}.mp3"))
        for i in range(7)
    ]

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


class ScoreCounter(pyrite.Renderable):
    font = pygame.Font()

    def __init__(
        self,
        player: Player,
        container: Container = None,
        enabled=True,
        layer: Layer = None,
        draw_index=0,
        position: pygame.Vector2 = (0, 0),
    ) -> None:
        super().__init__(container, enabled, layer, draw_index)
        self.player = player
        self.position = pygame.Vector2(position)
        self.size = pygame.Vector2(32, 32)

        self.surface = pygame.Surface(self.size)

    def get_rect(self) -> pygame.Rect:
        rect = pygame.Rect(size=self.size)
        rect.center = self.position
        return rect

    def render(self, delta_time: float) -> pygame.Surface:
        bg_color = pygame.Color("gray88")
        self.surface.fill(bg_color)
        score_draw = self.font.render(
            str(self.player.score),
            antialias=True,
            color=pygame.Color("black"),
            bgcolor=bg_color,
        )
        self.surface.blit(
            score_draw, score_draw.get_rect(center=self.surface.get_rect().center)
        )
        return self.surface


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


class Player:

    def __init__(self) -> None:
        self.score = 0


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
        self.size = pygame.Vector2(10, 400)

        self.surface = pygame.Surface(self.size)

        for index in range(8):
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

        self.court: Court = container

        self.position = pygame.Vector2(start_position)
        self.size = pygame.Vector2(16, 16)

        self.surface = pygame.Surface(self.size)
        self.surface.fill(pygame.Color("white"))

        self.max_velocity = 256
        self.velocity = pygame.Vector2(0, 0)

    def update(self, delta_time: float) -> None:
        self.position += self.velocity * delta_time

    def get_rect(self) -> pygame.Rect:
        rect = pygame.Rect((0, 0), self.size)
        rect.center = self.position
        return rect

    def render(self, delta_time: float) -> pygame.Surface:
        return self.surface


class Court(pyrite.Entity):
    wall_bounce_sounds: list[pygame.Sound] = [
        pygame.Sound(Path(f"examples/pong/assets/sounds/twoTone{i+1}.mp3"))
        for i in range(2)
    ]
    point_scored_sounds: list[pygame.Sound] = [
        pygame.Sound(Path(f"examples/pong/assets/sounds/spaceTrash{i+1}.mp3"))
        for i in range(5)
    ]

    def __init__(
        self,
        game_instance: pyrite.Game = None,
        enabled=True,
        court_size: pygame.Vector2 = None,
    ) -> None:
        super().__init__(game_instance, enabled)

        if court_size is None:
            court_size = pygame.Vector2(game_instance.window.size)

        self.size = pygame.Vector2(court_size)

        self.p1_paddle = self.create_paddle(10)

        self.p2_paddle = self.create_paddle(self.size.x - 20)

        self.net = Net(self)
        self.net.position = pygame.Vector2((self.size.x / 2) - (self.net.size.x / 2), 0)

        self.player1_controller: PaddleController = PlayerController(
            self, paddle=self.p1_paddle, control_keys=(pygame.K_w, pygame.K_s)
        )

        self.player2_controller: PaddleController = PlayerController(
            self, paddle=self.p2_paddle, control_keys=(pygame.K_UP, pygame.K_DOWN)
        )

        self.is_playing = False
        self.ball: Ball = Ball(self, False)

        self.player1 = Player()
        self.player2 = Player()
        self.score_zones = {
            self.player1: pygame.Rect(-10, 0, 10, self.size.y),
            self.player2: pygame.Rect(self.size.x + 10, 0, 10, self.size.y),
        }

        self.player1_scorebox = ScoreCounter(self.player1)
        self.player1_scorebox.position = pygame.Vector2((self.size.x / 2), 32)

    def enable(self, item):
        self.container.enable(item)

    def disable(self, item):
        self.container.disable(item)

    def update(self, delta_time: float) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if not self.is_playing:
                self.start()
                self.is_playing = True

        if self.is_playing:
            self.check_ball_collisions(self.ball)

    def check_ball_collisions(self, ball: Ball):
        self.check_ball_in_bounds(ball)
        self.check_ball_paddle_hit(
            ball,
            {
                self.p1_paddle: self.p1_paddle.get_rect(),
                self.p2_paddle: self.p2_paddle.get_rect(),
            },
        )
        self.check_ball_scored(ball, self.score_zones)

    def check_ball_in_bounds(self, ball: Ball):
        max_y = self.size.y - (ball.size.y / 2)
        min_y = ball.size.y / 2
        if ball.position.y > max_y or ball.position.y < min_y:
            # Deflect off the sides
            ball.velocity.y = -ball.velocity.y
            random.choice(self.wall_bounce_sounds).play()
        # Clamp position. This will prevent weird double bouncing from clipping the
        # sides
        ball.position.y = max(min_y, min(ball.position.y, max_y))

    def check_ball_paddle_hit(self, ball: Ball, paddles: dict[Paddle, pygame.Rect]):
        hit = ball.get_rect().collidedict(paddles, values=True)
        if hit is not None:
            ball.velocity.x = -ball.velocity.x

            paddle = hit[0]
            delta_x = ball.position.x - paddle.position.x
            sign = delta_x / abs(delta_x)
            ball.position.x += ((ball.size.x / 2) + (paddle.size.x / 2)) * sign
            random.choice(paddle.hit_sounds).play()

    def check_ball_scored(self, ball: Ball, score_zones: dict[Player, pygame.Rect]):
        scored = ball.get_rect().collidedict(score_zones, values=True)
        if scored is not None:
            scored_player = scored[0]
            scored_player.score += 1
            ball.enabled = False
            self.is_playing = False
            random.choice(self.point_scored_sounds).play()

    def start(self):
        self.ball.enabled = True
        self.ball.position = self.size.elementwise() / 2
        directions = [math.sin(math.pi / 4), -math.sin(math.pi / 4)]
        direction = pygame.Vector2(random.choice(directions), random.choice(directions))
        self.ball.velocity = direction * self.ball.max_velocity

    def create_paddle(self, x_pos: int) -> Paddle:
        paddle = Paddle(self)
        paddle.position = pygame.Vector2(x_pos, (self.size.y / 2) - (paddle.size.y / 2))
        return paddle


if __name__ == "__main__":
    with pyrite.Game(resolution=(800, 500)) as pong_game:
        pong_game.game_data.title = "Example Pong"
        court = Court(pong_game, court_size=(800, 400))
