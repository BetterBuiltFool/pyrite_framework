from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from ..services import CameraService
from ..enum import Layer
from ..events import OnEnable, OnDisable
from ..rendering import CameraRenderer
from ..rendering.viewport import Viewport
from ..transform import transform_component
from ..types import Camera as CameraBase, Renderable

if TYPE_CHECKING:
    from ..types import CameraViewBounds, TransformLike
    from ..types.projection import Projection
    from ..types.render_target import RenderTarget
    from ..transform import Transform
    from pygame.typing import Point


class Camera(CameraBase):

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
            if isinstance(transform, transform_component.TransformComponent):
                # If we're being passed something else's transform,
                # we'll just use that instead.
                self.transform = transform
            else:
                self.transform = transform_component.from_transform(self, transform)
        else:
            self.transform = transform_component.from_attributes(self, position)
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
        self.enabled = enabled
        self._zoom_level: float = 1
        CameraService.add_camera(self)

    @property
    def enabled(self) -> bool:
        return CameraService.is_enabled(self)

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = value
        if value:
            CameraService.enable(self)
            self.OnEnable(self)
        else:
            CameraService.disable(self)
            self.OnDisable(self)

    @property
    def zoom_level(self):
        return self._zoom_level

    @zoom_level.setter
    def zoom_level(self, zoom: float):
        self._zoom_level = zoom

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
