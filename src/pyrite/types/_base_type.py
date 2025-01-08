from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import src.pyrite._helper.instance as instance

if TYPE_CHECKING:
    from src.pyrite.types import Container


logger = logging.getLogger(__name__)


class _BaseType:

    def __init__(self, container: Container = None, enabled=True) -> None:
        if container is None:
            container = instance.get_game_instance()
        self.container: Container = container
        self.enabled = enabled

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = value
        # if self.container is None:
        #     self.container = instance.get_game_instance()
        if self.container is None:
            # logger.warning("No running game instance available.")
            return
        if value:
            self.container.enable(self)
        else:
            self.container.disable(self)
