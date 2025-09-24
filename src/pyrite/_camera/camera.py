from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from pyrite._services.camera_service import CameraServiceProvider as CameraService
from pyrite.enum import Layer
from pyrite.events import OnEnable, OnDisable
from pyrite._rendering.camera_renderer import CameraRendererProvider as CameraRenderer
from pyrite._rendering.viewport import Viewport
from pyrite._transform.transform_component import TransformComponent
from pyrite._types.camera import CameraBase
from pyrite._types.renderable import Renderable

if TYPE_CHECKING:
    from pygame.typing import Point
    from pyrite._types.view_bounds import CameraViewBounds
    from pyrite._types.protocols import RenderTarget, TransformLike
    from pyrite._types.projection import Projection
    from pyrite._transform.transform import Transform


class Camera(CameraBase):
    """
    Object for rendering a view to the display.

    ### Events:
    - OnEnable: Called when the object becomes enabled.
    - OnDisable: Called when the object becomes disabled.
    """

    def __init__(
        self,
        projection: Projection,
        position: Point = (0, 0),
        transform: TransformLike | None = None,
        render_targets: RenderTarget | Sequence[RenderTarget] | None = None,
        layer_mask: Sequence[Layer] | None = None,
        enabled=True,
    ) -> None:
        if transform is not None:
            if isinstance(transform, TransformComponent):
                # If we're being passed something else's transform,
                # we'll just use that instead.
                self.transform = transform
            else:
                self.transform = TransformComponent.from_transform(self, transform)
        else:
            self.transform = TransformComponent.from_attributes(self, position)
        self.projection = projection
        if render_targets is None:
            render_targets = [Viewport.DEFAULT]
        if not isinstance(render_targets, Sequence):
            render_targets = [render_targets]
        self.render_targets: Sequence[RenderTarget] = render_targets
        self._viewports = [
            viewport for viewport in render_targets if isinstance(viewport, Viewport)
        ]
        if layer_mask is None:
            layer_mask = ()
        self.layer_mask: Sequence[Layer] = layer_mask
        self.OnEnable = OnEnable(self)
        self.OnDisable = OnDisable(self)
        self._enabled = False
        self.enabled = enabled
        self._zoom_level: float = 1
        CameraService.add_camera(self)

    @property
    def enabled(self) -> bool:
        return CameraService.is_enabled(self)

    @enabled.setter
    def enabled(self, enabled: bool) -> None:
        if enabled:
            CameraService.enable(self)
            if not self._enabled:
                self.OnEnable(self)
        else:
            CameraService.disable(self)
            if self._enabled:
                self.OnDisable(self)
        self._enabled = enabled

    @property
    def zoom_level(self):
        return self._zoom_level

    @zoom_level.setter
    def zoom_level(self, zoom_level: float):
        self._zoom_level = zoom_level

    def refresh(self):
        CameraService.refresh(self)

    def cull(self, renderable: Renderable) -> bool:
        bounds = renderable.get_bounds()
        return self.get_view_bounds().contains(bounds)

    def get_view_bounds(self) -> CameraViewBounds:
        return CameraService.get_view_bounds(self)

    def get_viewports(self) -> list[Viewport]:
        return self._viewports

    def render(self, delta_time: float, render_target: RenderTarget):
        CameraRenderer.render(delta_time, self, render_target)

    def to_local(self, point: Transform) -> Transform:
        return CameraService.to_local(self, point)

    def to_eye(self, point: Transform) -> Transform:
        return CameraService.to_eye(self, point)

    def to_world(self, point: Transform) -> Transform:
        return CameraService.to_world(self, point)

    # def screen_to_world(self, point: Point, viewport_index: int = 0) -> Point:
    #     return CameraService.screen_to_world(self, point, viewport_index)

    # def screen_to_world_clamped(
    #     self, point: Point, viewport_index: int = 0
    # ) -> Point | None:
    #     return CameraService.screen_to_world_clamped(self, point, viewport_index)

    def zoom(self, zoom_level: float):
        CameraService.zoom(self, zoom_level)
