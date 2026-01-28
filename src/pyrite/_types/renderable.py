from __future__ import annotations

from abc import abstractmethod, ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyrite._types.camera import Camera
    from pyrite._types.bounds import CullingBounds
    from pyrite.enum import Layer


class Renderable(ABC):
    """
    Base class for any renderable object in pyrite.
    """

    draw_index: int
    _layer: Layer

    @property
    @abstractmethod
    def layer(self) -> Layer:
        pass

    @layer.setter
    @abstractmethod
    def layer(self, layer: Layer):
        pass

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
