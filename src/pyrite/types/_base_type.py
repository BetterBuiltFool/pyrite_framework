from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import src.pyrite._helper.defaults as defaults

if TYPE_CHECKING:
    from src.pyrite.types import Container


logger = logging.getLogger(__name__)


class _BaseType:

    def __init__(self, container: Container = None, enabled=True) -> None:
        if container is None:
            container = defaults.get_default_container()
        self.container: Container = container
        self.enabled = enabled

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = value
        # if self.container is None:
        if self.container is None:
            logger.warning(f"{self} has no container for enabling/disabling.")
            return
        if value:
            self.container.enable(self)
        else:
            self.container.disable(self)
