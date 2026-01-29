from __future__ import annotations

from typing import TYPE_CHECKING

from pyrite.enum import RenderLayers
from pyrite.core.enableable import Enableable
from pyrite.core.render_system import RenderManager
from pyrite._types.renderable import Renderable

if TYPE_CHECKING:
    from pyrite.enum import Layer


class BaseRenderable(Renderable, Enableable[RenderManager], manager=RenderManager):
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
        super().__init__(enabled)

    def __init_subclass__(cls, **kwds) -> None:
        return super().__init_subclass__(manager=RenderManager, **kwds)

    @property
    def layer(self) -> Layer:
        return self._layer

    @layer.setter
    def layer(self, layer: Layer):
        if self._layer is not layer:
            enabled = self.enabled
            # This allows us to update within the renderer without firing
            # on enable/disable events.
            RenderManager.disable(self)
            self._layer = layer
            if enabled:
                RenderManager.enable(self)
