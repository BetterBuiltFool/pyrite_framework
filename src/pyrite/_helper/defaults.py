from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.pyrite.game import Game

_instance: Game = None


def get_game_instance() -> Game | None:
    return _instance


def set_game_instance(game_instance: Game):
    global _instance
    _instance = game_instance
