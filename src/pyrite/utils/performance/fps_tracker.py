from __future__ import annotations

import sys
from typing import Self, TYPE_CHECKING

from src.pyrite.types.entity import Entity

if TYPE_CHECKING:
    from src.pyrite.game import Game
    from src.pyrite.types import Container


class FPSTracker(Entity):
    _instance: FPSTracker = None

    def __new__(cls, *args, **kwds) -> Self:
        instance = cls._instance
        if instance is None:
            instance = super().__new__(FPSTracker)
            cls._instance = instance
        return instance

    def __init__(self, container: Container = None, enabled=True) -> None:
        super().__init__(container, enabled)
        self.max: float = 0
        self.min: float = sys.float_info.max
        self.max_entities: int = 0
        self.max_renderables: int = 0

    def post_update(self, delta_time: float) -> None:
        game_instance: Game = self.container

        current_fps = game_instance.clock.get_fps()

        self.max = max(current_fps, self.max)
        if current_fps > 0:  # To bypass startup lag
            self.min = min(current_fps, self.min)

        self.max_entities = max(
            self.max_entities,
            game_instance.entity_manager.get_number_entities() - 1,
        )

        self.max_renderables = max(
            self.max_renderables, game_instance.renderer.get_number_renderables()
        )
