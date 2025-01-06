from abc import abstractmethod
from src.pyrite.types.entity import Entity


class Service(Entity):

    @abstractmethod
    def __init__(self, game_instance=None, enabled=True) -> None:
        super().__init__(game_instance, enabled)
