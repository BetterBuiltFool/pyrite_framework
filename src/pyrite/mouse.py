from __future__ import annotations

from typing import TYPE_CHECKING

from . import game

import pygame

if TYPE_CHECKING:
    pass


def get_pos() -> tuple[int, int]:
    mouse_screen_pos = pygame.mouse.get_pos()
    game_instance = game.get_game_instance()
    if game_instance is None:
        return mouse_screen_pos
    return game_instance.renderer.screen_to_world(
        mouse_screen_pos, game_instance.window
    )
