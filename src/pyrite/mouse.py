from __future__ import annotations

from typing import TYPE_CHECKING

from . import game

import pygame

if TYPE_CHECKING:
    from pygame.typing import Point


def get_pos() -> Point:
    """
    Gives the position of the mouse in world space. If the mouse is not in a valid
    position (i.e., in a space without any rendering) the screen pos will be given.

    :return: A point in 2D world space.
    """
    mouse_screen_pos = pygame.mouse.get_pos()
    game_instance = game.get_game_instance()
    if game_instance is None:
        return mouse_screen_pos
    return game_instance.renderer.screen_to_world(
        mouse_screen_pos, game_instance.window
    )
