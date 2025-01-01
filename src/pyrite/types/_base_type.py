import logging

# from ..game import get_game_instance
import src.pyrite.game as game


logger = logging.getLogger(__name__)


class _BaseType:

    def __init__(self, game_instance=None, enabled=True) -> None:
        self.game_instance: game.Game = game_instance
        self.enabled = enabled

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
