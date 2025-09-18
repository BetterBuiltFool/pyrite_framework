from __future__ import annotations

from typing import TYPE_CHECKING

from ..enum import RenderLayers
from ..events import OnEnable, OnDisable
from ..core import render_system
from pyrite._types.renderable import Renderable

if TYPE_CHECKING:
    from ..enum import Layer


class BaseRenderable(Renderable):
    """
    Base class for any object that renders to the screen.

    ### Events:
    - OnEnable: Called when the object becomes enabled.
    - OnDisable: Called when the object becomes disabled.
    """

    def __init__(
        self,
        enabled=True,
        layer: Layer | None = None,
        draw_index=0,
    ) -> None:
        if layer is None:
            layer = RenderLayers.MIDGROUND
        self._layer: Layer = layer
        self.draw_index = draw_index
        """
        (The following is only true for default renderer; Others may vary)

        Indexer for draw order within a layer.
        Negative indexes are relative to the end.
        Renderables in the same layer with the same index may be drawn in any order.
        """
        self.OnEnable = OnEnable(self)
        self.OnDisable = OnDisable(self)
        self.enabled = enabled

    @property
    def enabled(self) -> bool:
        return render_system.is_enabled(self)

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = value
        if value:
            self.on_preenable()
            if render_system.enable(self):
                self.OnEnable(self)
                self.on_enable()
        else:
            self.on_predisable()
            if render_system.disable(self):
                self.OnDisable(self)
                self.on_disable()

    @property
    def layer(self) -> Layer:
        return self._layer

    @layer.setter
    def layer(self, new_layer: Layer):
        if self._layer is not new_layer:
            enabled = self.enabled
            # This allows us to update within the renderer without firing
            # on enable/disable events.
            render_system.disable(self)
            self._layer = new_layer
            if enabled:
                render_system.enable(self)
