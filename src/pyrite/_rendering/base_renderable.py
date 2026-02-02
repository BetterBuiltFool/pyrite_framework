from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from pyrite.enum import RenderLayers
from pyrite.core.enableable import Enableable
from pyrite.core.render_system import RenderManager

if TYPE_CHECKING:
    from pyrite.enum import Layer
    from pyrite._types.camera import Camera
    from pyrite._types.bounds import CullingBounds


class BaseRenderable(ABC, Enableable[RenderManager], manager=RenderManager):
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

    @abstractmethod
    def get_bounds(self) -> CullingBounds:
        """
        Returns a Bounds object that describes the occupied space of the renderable for
        the sake of camera culling.
        """
        pass

    @abstractmethod
    def render(self, camera: Camera):
        """
        Causes the Renderable to be rendered to the given camera. Typically calls upon
        some renderer class that knows how to handle its data.

        :param camera: A camera-type object to be drawn to.
        """
        pass
