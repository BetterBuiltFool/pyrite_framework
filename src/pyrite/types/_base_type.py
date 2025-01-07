from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import src.pyrite._helper.instance as instance

if TYPE_CHECKING:
    from src.pyrite.game import Game


logger = logging.getLogger(__name__)


class _BaseType:

    def __init__(self, game_instance=None, enabled=True) -> None:
        if game_instance is None:
            game_instance = instance.get_game_instance()
        self.game_instance: Game = game_instance
        self.enabled = enabled

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = value
        if self.game_instance is None:
            self.game_instance = instance.get_game_instance()
        if self.game_instance is None:
            # logger.warning("No running game instance available.")
            return
        if value:
            self.game_instance.enable(self)
        else:
            self.game_instance.disable(self)
