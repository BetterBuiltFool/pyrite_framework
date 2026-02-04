from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, TYPE_CHECKING


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


class Camera(Protocol):
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
    def projection(self) -> Projection: ...

    @projection.setter
    def projection(self, projection: Projection) -> None: ...

    @property
    def zoom_level(self) -> float: ...

    @zoom_level.setter
    def zoom_level(self, zoom_level: float): ...

    def cull(self, renderable: Renderable) -> bool:
        """
        Compares the bounds of the renderable to the camera's view bounds to determine
        if the renderable should be rendered.

        :param renderable: Any renderable item to be drawn.
        :return: True if the renderable is visible and should be drawn, otherwise False.
        """
        ...

    def get_view_bounds(self) -> CameraViewBounds:
        """
        Gets the bounds object that represents the visible space of the camera.

        :return: A CameraViewBounds object describing the viewed space.
        """
        ...

    def get_viewports(self) -> Sequence[Viewport]:
        """
        Gets a sequence of viewports targeted by the camera.

        :return: A sequence of viewports, empty if there are none.
        """
        ...

    def render(self, render_target: RenderTarget):
        """
        Renders the camera view to the render target

        :param render_target: _description_
        """
        ...

    @property
    def enabled(self) -> bool: ...

    @enabled.setter
    def enabled(self, enabled: bool) -> None: ...

    def on_preenable(self): ...

    def on_enable(self): ...

    def on_predisable(self): ...

    def on_disable(self): ...
