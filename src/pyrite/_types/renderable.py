from __future__ import annotations

from abc import abstractmethod, ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyrite._types.camera import Camera
    from pyrite._types.bounds import CullingBounds
    from pyrite.enum import Layer
    from pyrite.events import OnEnable as EventOnEnable
    from pyrite.events import OnDisable as EventOnDisable


class Renderable(ABC):
    """
    Base class for any renderable object in pyrite.
    """

    draw_index: int
    _layer: Layer
    OnEnable: EventOnEnable
    OnDisable: EventOnDisable

    @property
    @abstractmethod
    def enabled(self) -> bool:
        pass

    @enabled.setter
    @abstractmethod
    def enabled(self, enabled: bool) -> None:
        pass

    @property
    @abstractmethod
    def layer(self) -> Layer:
        pass

    @layer.setter
    @abstractmethod
    def layer(self, layer: Layer):
        pass

    def on_preenable(self):
        """
        Event called just before the object is enabled.
        Useful if the object needs to be modified before going through the enabling
        process.
        Does NOT guarantee the object is not already enabled.

        """

    def on_enable(self):
        """
        Event called just after the object has been enabled.
        Useful for when an object needs to perform actions on other objects immediately
        after being enabled.
        Guarantees the object is now enabled, and only runs when the object was
        previously disabled.
        """

    def on_predisable(self):
        """
        Event called just before the object is disabled.
        Useful if the object needs to perform some kind of cleanup action before
        disabling.
        Does NOT guarantee the object has not already been disabled.
        """

    def on_disable(self):
        """
        Event called just after the object has been disabled.
        Useful if the object needs to perform and action, like cleanup, only after it
        has been disabled.
        Guarantees the object is now disabled, and that the object was previously
        disabled.
        """

    @abstractmethod
    def get_bounds(self) -> CullingBounds:
        """
        Returns a Bounds object that describes the occupied space of the renderable for
        the sake of camera culling.
        """
        pass

    @abstractmethod
    def render(self, delta_time: float, camera: Camera):
        """
        Causes the Renderable to be rendered to the given camera. Typically calls upon
        some renderer class that knows how to handle its data.

        :param delta_time: Time passed since last frame. Can be ignored by the concrete
            method but must be accepted.
        :param camera: A camera-type object to be drawn to.
        """
        pass
