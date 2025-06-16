from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, TypeVar

from . import camera_service
from ..enum import Layer
from ..rendering import CameraRenderer, RectBounds, Viewport
from ..transform import transform_component
from ..types import CameraBase, Renderable
from .._helper import defaults

if TYPE_CHECKING:
    from ..types import CameraViewBounds, Container, TransformProtocol
    from ..types.projection import Projection as ProjectionType
    from ..types.render_target import RenderTarget
    from ..transform import Transform
    from pygame.typing import Point

    Projection = TypeVar("Projection", bound=ProjectionType)


class Camera(CameraBase):

    def __init__(
        self,
        projection: Projection,
        position: Point = (0, 0),
        transform: TransformProtocol = None,
        render_targets: RenderTarget | Sequence[RenderTarget] = None,
        layer_mask: tuple[Layer] = None,
        container: Container = None,
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
        self.render_targets: Sequence[Viewport] = render_targets
        self._viewports = [
            viewport for viewport in render_targets if isinstance(viewport, Viewport)
        ]
        if layer_mask is None:
            layer_mask = ()
        self.layer_mask = layer_mask
        self.enabled = enabled
        self._zoom_level = 1
        if container is None:
            container = defaults.get_default_container()
        self.container = container
        camera_service.CameraService.add_camera(self)

    @property
    def enabled(self) -> bool:
        return camera_service.CameraService.is_enabled(self)

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = value
        if value:
            camera_service.CameraService.enable(self)
        else:
            camera_service.CameraService.disable(self)

    @property
    def zoom_level(self):
        return self._zoom_level

    def refresh(self):
        camera_service.CameraService.refresh(self)

    def cull(self, renderable: Renderable) -> bool:
        bounds = renderable.get_bounds()
        return self.get_view_bounds().contains(bounds)

    def get_bounds(self) -> RectBounds:
        return camera_service.CameraService.get_bounds(self)

    def get_view_bounds(self) -> CameraViewBounds:
        return camera_service.CameraService.get_view_bounds(self)

    def get_viewports(self) -> list[Viewport]:
        """
        Gets a list of viewports targeted by the camera.

        :return: A list of viewports, empty if there are none.
        """
        return self._viewports

    def render(self, delta_time, viewport: Viewport):
        CameraRenderer.render(delta_time, self, viewport)

    def to_local(self, point: Transform) -> Transform:
        return camera_service.CameraService.to_local(self, point)

    def to_eye(self, point: Transform) -> Transform:
        return camera_service.CameraService.to_eye(self, point)

    def to_world(self, point: Transform) -> Transform:
        return camera_service.CameraService.to_world(self, point)

    def screen_to_world(self, point: Point, viewport_index: int = 0) -> Point:
        return camera_service.CameraService.screen_to_world(self, point, viewport_index)

    def screen_to_world_clamped(
        self, point: Point, viewport_index: int = 0
    ) -> Point | None:
        return camera_service.CameraService.screen_to_world_clamped(
            self, point, viewport_index
        )

    def zoom(self, zoom_level: float):
        camera_service.CameraService.zoom(self, zoom_level)
