from __future__ import annotations

from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from pyrite._types.camera import Camera
    from pyrite._types.bounds import CullingBounds
    from pyrite.enum import Layer
    from pyrite.events import OnEnable as OnEnableEvent, OnDisable as OnDisableEvent


class Renderable(Protocol):
    """
    Base class for any renderable object in pyrite.
    """

    draw_index: int
    _layer: Layer

    OnEnable: OnEnableEvent
    OnDisable: OnDisableEvent

    @property
    def layer(self) -> Layer: ...

    @layer.setter
    def layer(self, layer: Layer): ...

    def get_bounds(self) -> CullingBounds:
        """
        Returns a Bounds object that describes the occupied space of the renderable for
        the sake of camera culling.
        """
        ...

    def render(self, camera: Camera):
        """
        Causes the Renderable to be rendered to the given camera. Typically calls upon
        some renderer class that knows how to handle its data.

        :param camera: A camera-type object to be drawn to.
        """
        ...

    def on_preenable(self): ...

    def on_enable(self): ...

    def on_predisable(self): ...

    def on_disable(self): ...
