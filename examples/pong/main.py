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

pygame.init()  # Game will call this, too, but we need several modules early.


class Paddle(pyrite.Entity, pyrite.Renderable):
    """
    The actual play pieces of the game. These move up and down to try and hit the ball.
    """

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
            self.size.y / 2,
            min(self.position.y, (self.container.size.y - (self.size.y / 2))),
        )

    def get_rect(self) -> pygame.Rect:
        # Personal preference, really, but I tend to prefer using position-on-center
        # instead of default topleft
        rect = pygame.Rect((0, 0), self.size)
        rect.center = self.position
        return rect
        # return pygame.Rect(self.position, self.size)

    def render(self, delta_time: float) -> pygame.Surface:
        return self.surface


class PaddleController(Protocol):
    """
    Simple protocol for the Court to allow know that the controller always has a paddle
    attribute.

    This isn't important if you don't use type hints, but I find them immensely helpful.
    """

    paddle: Paddle


class ScoreCounter(pyrite.Renderable):
    """
    A basic object to display each player's score on the screen.
    """

    font = pygame.Font(size=48)

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
        self.size = pygame.Vector2(64, 64)

        self.surface = pygame.Surface(self.size)

    def get_rect(self) -> pygame.Rect:
        rect = pygame.Rect((0, 0), self.size)
        rect.center = self.position
        return rect

    def render(self, delta_time: float) -> pygame.Surface:
        bg_color = pygame.Color("black")
        self.surface.fill(bg_color)
        score_draw = self.font.render(
            str(self.player.score),
            antialias=True,
            color=pygame.Color("grey88"),
            bgcolor=bg_color,
        )
        self.surface.blit(
            score_draw, score_draw.get_rect(center=self.surface.get_rect().center)
        )
        return self.surface


class PlayerController(pyrite.Entity):
    """
    The player controller listens for key input, and modifies the paddle velocity based
    on it.
    """

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
        # Call this in pre_update to ensure that the velocity is captured in the same
        # frame. Otherwise, we might see some frame delay.
        keys = pygame.key.get_pressed()
        y = 0
        if keys[self.up_key]:
            y -= 1
        if keys[self.down_key]:
            y += 1
        if self.paddle is not None:
            self.paddle.velocity = self.paddle.max_speed * y


class AIController(pyrite.Entity):
    """
    A very simple AI player. Works for either paddle.

    Has a basic strategy where it tries to chase the ball whenever it is on its half of
    the court.

    To defeat it, just hit the ball until the ball is moving faster than the paddle can.
    It can't anticipate the ball.
    """

    def __init__(
        self,
        container: Court = None,
        enabled=True,
        paddle: Paddle = None,
    ) -> None:
        super().__init__(container, enabled)
        self.court = container
        self.paddle = paddle

    def update(self, delta_time: float) -> None:
        if not self.court.is_playing:
            # Center up if the ball is out of play.
            self.paddle.position.y = self.court.size.y / 2
            self.paddle.velocity = 0
            return
        if abs(self.paddle.position.x - self.court.ball.position.x) > (
            # Tweak this to change how far the ball can be to chase
            (self.court.size.x / 2)
        ):
            # Stop where it is if the ball is off of its side of the court
            self.paddle.velocity = 0
            return
        ball_delta_y = self.court.ball.position.y - self.paddle.position.y
        # Move the paddle towards the ball if it's too far.
        if ball_delta_y > 8:
            self.paddle.velocity = self.paddle.max_speed
        elif ball_delta_y < 8:
            self.paddle.velocity = -self.paddle.max_speed
        else:
            self.paddle.velocity = 0


class Player:
    """
    Super basic class, just for tracking the player's score.
    """

    def __init__(self) -> None:
        self.score = 0


class Net(pyrite.Renderable):
    """
    A piece of set dressing. Didn't need to be this specific, could have made it take a
    surface from elsewhere and been more generic.
    """

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
    """
    The actual most important piece of the game.
    """

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
        # All it needs to do is move. Everything else is another object's job.
        self.position += self.velocity * delta_time

    def get_rect(self) -> pygame.Rect:
        rect = pygame.Rect((0, 0), self.size)
        rect.center = self.position
        return rect

    def render(self, delta_time: float) -> pygame.Surface:
        return self.surface

    def speed_up(self):
        """
        Increases the ball's speed by 5%.

        You can tweak that number to affect the difficulty, or change how it's
        calculated to chang ethe difficulty ramp.
        """
        speed = self.velocity.magnitude()
        direction = self.velocity.normalize()
        speed *= 1.05
        self.velocity = speed * direction


class Court(pyrite.Entity):
    """
    The actual level on which the game plays.
    This contains all of the game objects, and allows them to reference eachother as
    needed.

    The court also controls aspects of the game like collision. This reduces the need
    for the game objects to know much about eachother.
    """

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
            # Fallback system in case no size is specified when building the court.
            court_size = pygame.Vector2(game_instance.window.size)

        self.size = pygame.Vector2(court_size)

        inset = 15  # Distance from court edge for paddle

        self.p1_paddle = self.create_paddle(inset)

        self.p2_paddle = self.create_paddle(self.size.x - inset)

        self.net = Net(self)
        self.net.position = pygame.Vector2((self.size.x / 2) - (self.net.size.x / 2), 0)

        self.player1_controller: PaddleController = PlayerController(
            self, paddle=self.p1_paddle, control_keys=(pygame.K_w, pygame.K_s)
        )

        # ---------------------------------------------------------------------------------------------------
        #
        # Swap these two to do 2 player
        #

        # self.player2_controller: PaddleController = PlayerController(
        #     self, paddle=self.p2_paddle, control_keys=(pygame.K_UP, pygame.K_DOWN)
        # )
        self.player2_controller: PaddleController = AIController(
            self, paddle=self.p2_paddle
        )
        # ---------------------------------------------------------------------------------------------------

        self.is_playing = False
        self.ball: Ball = Ball(self, False)

        self.player1 = Player()
        self.player2 = Player()

        # These are the goals.
        # If the ball ends up in one of these goals, that player gets a point.
        # Could have made these discrete objects, but a rectangle was sufficient and
        # made collision easier.
        self.score_zones = {
            self.player2: pygame.Rect(-10, 0, 10, self.size.y),
            self.player1: pygame.Rect(self.size.x + 10, 0, 10, self.size.y),
        }

        self.player1_scorebox = ScoreCounter(self.player1)
        self.player1_scorebox.position = pygame.Vector2(
            (self.size.x / 4), self.size.y + 64
        )

        self.player2_scorebox = ScoreCounter(self.player2)
        self.player2_scorebox.position = pygame.Vector2(
            (3 * self.size.x / 4), self.size.y + 64
        )

    def enable(self, item):
        # In this case, the container should be the game instance, but containers can
        # stack (theoretically) infinitely
        self.container.enable(item)

    def disable(self, item):
        self.container.disable(item)

    def update(self, delta_time: float) -> None:
        # Looks for someone to press Space to start. Will not allow a restart until the
        # ball goes out of play.
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if not self.is_playing:
                self.start()
                self.is_playing = True

        if self.is_playing:
            self.check_ball_collisions(self.ball)

    def check_ball_collisions(self, ball: Ball):
        """
        Runs collision detect on all of the important things to compare the ball to.
        """
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
        """
        Makes sure the ball is in a valid area of play.

        Bounces the ball off the sides if needed.
        Plays a wall hit sound when it does so.
        """
        max_y = self.size.y - (ball.size.y / 2)
        min_y = ball.size.y / 2
        if ball.position.y > max_y or ball.position.y < min_y:
            # Deflect off the sides
            ball.velocity.y = -ball.velocity.y
            ball.speed_up()
            random.choice(self.wall_bounce_sounds).play()
        # Clamp position. This will prevent weird double bouncing from clipping the
        # sides
        ball.position.y = max(min_y, min(ball.position.y, max_y))

    def check_ball_paddle_hit(self, ball: Ball, paddles: dict[Paddle, pygame.Rect]):
        """
        Checks to see if the ball hit a paddle.

        If so, reflect it, play a paddle hit sound, and make sure the ball isn't still
        inside the paddle (This would cause some weird multiple reflections)
        """
        # Make sure values=True in collidedict here, as that's where our Rects are
        hit = ball.get_rect().collidedict(paddles, values=True)
        if hit is not None:
            # This means we hit something

            # Reflect the ball
            ball.velocity.x = -ball.velocity.x

            paddle = hit[0]  # Get the paddle so we can do stuff with it.

            # This makes sure we don't collide again next frame before the ball can
            # move out.
            # Another way of doing this would be to disable paddle collisions on the
            # ball for a few frames, but this was easier and sufficient.
            delta_x = ball.position.x - paddle.position.x
            sign = delta_x / abs(delta_x)
            ball.position.x += ((ball.size.x / 2) + (paddle.size.x / 2)) * sign

            ball.speed_up()

            random.choice(paddle.hit_sounds).play()

    def check_ball_scored(self, ball: Ball, score_zones: dict[Player, pygame.Rect]):
        """
        Checks the ball against the goals.

        If we're in a goal, award a point to the respective player.
        """
        scored = ball.get_rect().collidedict(score_zones, values=True)
        if scored is not None:
            # Award the player a point
            scored_player = scored[0]
            scored_player.score += 1
            # Hide the ball. We don't need it again until next round.
            ball.enabled = False
            # End the round
            self.is_playing = False
            # Play a sound so the players know the round is over
            random.choice(self.point_scored_sounds).play()

    def start(self):
        """
        Does the setup for a new round.
        """
        # Allow the ball to render and move again
        self.ball.enabled = True
        # Put the ball back in the middle of the court
        self.ball.position = (
            self.size.elementwise() / 2
        )  # Equivalent to setting it to a rect's center, but this is sufficient.
        # Pick a random direction, a diagonal.
        directions = [math.sin(math.pi / 4), -math.sin(math.pi / 4)]
        direction = pygame.Vector2(random.choice(directions), random.choice(directions))
        # Set the ball of in that direction at its max speed.
        self.ball.velocity = direction * self.ball.max_velocity

    def create_paddle(self, x_pos: int) -> Paddle:
        """
        A helper function to create a paddle at the given x position.
        This saves us a bit of effort by ensuring both paddles are created at the same
        y pos.
        """
        paddle = Paddle(self)
        paddle.position = pygame.Vector2(x_pos, (self.size.y / 2))
        return paddle


if __name__ == "__main__":
    with pyrite.Game(resolution=(800, 500)) as pong_game:
        pong_game.game_data.title = "Example Pong"
        # You could also open up on a menu screen, but that's for a different lesson.
        court = Court(pong_game, court_size=(800, 400))
