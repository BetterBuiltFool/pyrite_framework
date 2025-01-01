from abc import ABC

# from ..game import get_game_instance
import src.pyrite.game as game


class _BaseType(ABC):

    def __init__(self) -> None:
        self._enabled: bool = True

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = value
        game_instance = game.get_game_instance()
        if value:
            game_instance.enable(self)
        else:
            game_instance.disable(self)
