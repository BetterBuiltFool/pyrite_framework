from __future__ import annotations

from abc import abstractmethod, ABC
from typing import TYPE_CHECKING

from ..core import renderer
from .._helper import defaults

import pygame

if TYPE_CHECKING:
    from . import Container, CameraBase
    from ..enum import Layer


class Renderable(ABC):
    """
    Base class for any renderable object in pyrite.
    """

    def __init__(
        self,
        container: Container = None,
        enabled=True,
        layer: Layer = None,
        draw_index=0,
    ) -> None:
        self._layer: Layer = layer
        self.draw_index = draw_index
        """
        (The following is only true for default renderer; Others may vary)

        Indexer for draw order within a layer.
        Negative indexes are relative to the end.
        Renderables in the same layer with the same index may be drawn in any order.
        """
        if container is None:
            container = defaults.get_default_container()
        self.container: Container = container
        self.enabled = enabled

    @property
    def enabled(self) -> bool:
        return renderer.is_enabled(self)

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = value
        if self.container is None:
            return
        if value:
            self.on_preenable()
            if renderer.enable(self):
                self.on_enable()
        else:
            self.on_predisable()
            if renderer.disable(self):
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
            renderer.disable(self)
            self._layer = new_layer
            if enabled:
                renderer.enable(self)

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
    def cull(self, delta_time: float, camera: CameraBase) -> bool:
        """
        Determines if the renderable is seen by the camera and thus should be rendered.
        Typically calls upon some renderer class that knows how to handle its data.

        :param delta_time: Time passed since last frame. Can be ignored by the concrete
            method but must be accepted.
        :param camera: The camera being tested against.
        :return: True if the renderable is visible to the camera, otherwise False
        """

    @abstractmethod
    def render(self, delta_time: float, camera: CameraBase):
        """
        Causes the Renderable to be rendered to the given camera. Typically calls upon
        some renderer class that knows how to handle its data.

        :param delta_time: Time passed since last frame. Can be ignored by the concrete
            method but must be accepted.
        :param camera: A camera-type object to be drawn to.
        """
        pass

    @abstractmethod
    def get_rect(self) -> pygame.Rect:
        """
        Return a rectangle representing the area the rendered surface is expected to
        take up.

        :return: _description_
        """
        pass
