from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from pyrite._types.view_bounds import CameraViewBounds
    from pyrite._types.renderable import Renderable
    from pyrite._types.projection import Projection
    from pyrite._types.protocols import RenderTarget
    from pyrite._rendering.viewport import Viewport
    from pyrite.enum import Layer
    from pyrite.events import OnEnable as EventOnEnable
    from pyrite.events import OnDisable as EventOnDisable
    from pyrite._component.transform_component import TransformComponent


class Camera(ABC):
    """
    Defines the important attributes of a camera for the sake of drawing onto its
    surface.

    Can be constructed from the window.
    """

    layer_mask: Sequence[Layer]
    render_targets: Sequence[RenderTarget]
    transform: TransformComponent

    OnEnable: EventOnEnable
    OnDisable: EventOnDisable

    @property
    @abstractmethod
    def projection(self) -> Projection:
        pass

    @projection.setter
    @abstractmethod
    def projection(self, projection: Projection) -> None:
        pass

    @property
    @abstractmethod
    def zoom_level(self) -> float:
        pass

    @zoom_level.setter
    @abstractmethod
    def zoom_level(self, zoom_level: float):
        pass

    @abstractmethod
    def refresh(self):
        """
        Returns the camera to a state that is ready for rendering.
        """
        pass

    @abstractmethod
    def cull(self, renderable: Renderable) -> bool:
        """
        Compares the bounds of the renderable to the camera's view bounds to determine
        if the renderable should be rendered.

        :param renderable: Any renderable item to be drawn.
        :return: True if the renderable is visible and should be drawn, otherwise False.
        """
        pass

    @abstractmethod
    def get_view_bounds(self) -> CameraViewBounds:
        """
        Gets the bounds object that represents the visible space of the camera.

        :return: A CameraViewBounds object describing the viewed space.
        """

    @abstractmethod
    def get_viewports(self) -> Sequence[Viewport]:
        """
        Gets a sequence of viewports targeted by the camera.

        :return: A sequence of viewports, empty if there are none.
        """
        pass

    @abstractmethod
    def render(self, render_target: RenderTarget):
        """
        Renders the camera view to the render target

        :param render_target: _description_
        """
        pass
