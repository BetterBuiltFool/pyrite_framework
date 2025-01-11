from __future__ import annotations
from collections.abc import Callable
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.pyrite.game import Game
    from src.pyrite.types import Container

_instance: Game = None


def get_game_instance() -> Game | None:
    return _instance


def set_game_instance(game_instance: Game):
    global _instance
    _instance = game_instance


_default_container_getter = get_game_instance


def get_default_container() -> Container | None:
    return _default_container_getter()


def set_default_container_type(getter: Callable):
    """
    Sets the variable that is called by get_default_container.

    :param getter: A callable that returns a container or None.
    """
    global _default_container_getter
    _default_container_getter = getter
