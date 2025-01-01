from abc import ABC
import logging

# from ..game import get_game_instance
import src.pyrite.game as game


logger = logging.getLogger(__name__)


class _BaseType(ABC):

    def __init__(self) -> None:
        self.game_instance: game.Game = None
        self._enabled: bool = True
        self.enabled = True

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = value
        if self.game_instance is None:
            self.game_instance = game.get_game_instance()
        if self.game_instance is None:
            logger.warning("No running game instance available.")
            return
        if value:
            self.game_instance.enable(self)
        else:
            self.game_instance.disable(self)
