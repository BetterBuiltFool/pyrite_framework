from __future__ import annotations

from typing import TYPE_CHECKING

from .._helper import defaults

if TYPE_CHECKING:
    from . import Container


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
            return
        if value:
            self.on_preenable()
            self.container.enable(self)
            self.on_enable()
        else:
            self.on_predisable()
            self.container.disable(self)
            self.on_disable()

    def on_preenable(self): ...

    def on_enable(self): ...

    def on_predisable(self): ...

    def on_disable(self): ...
