from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, TypeVar

from .camera_service import CameraService
from ..rendering.viewport import Viewport
from ..enum import Layer
from ..rendering.camera_renderer import CameraRenderer
from ..rendering.rect_bounds import RectBounds
from ..transform import transform_component
from ..types import CameraBase, Renderable
from .._helper import defaults

import pygame

if TYPE_CHECKING:
    from ..types import CameraViewBounds, Container, TransformProtocol
    from ..types.projection import Projection
    from ..transform import Transform
    from pygame.typing import Point

    P = TypeVar("P", bound=Projection)


class Camera(CameraBase):

    def __init__(
        self,
        projection: P,
        position: Point = (0, 0),
        transform: TransformProtocol = None,
        viewports: Viewport | Sequence[Viewport] = None,
        smooth_scale: bool = False,
        layer_mask: tuple[Layer] = None,
        container: Container = None,
        enabled=True,
        draw_index: int = 0,
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
        self._smooth_scale = smooth_scale
        self._scale_method = (
            pygame.transform.scale if not smooth_scale else pygame.transform.smoothscale
        )
        if viewports is None:
            viewports = [Viewport.DEFAULT]
        if not isinstance(viewports, Sequence):
            viewports = [viewports]
        self.viewports: Sequence[Viewport] = viewports
        self.draw_index = draw_index
        if layer_mask is None:
            layer_mask = ()
        self.layer_mask = layer_mask
        self.enabled = enabled
        self._zoom_level = 1
        if container is None:
            container = defaults.get_default_container()
        self.container = container
        CameraService.add_camera(self)

    @property
    def enabled(self) -> bool:
        return CameraService.is_enabled(self)

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = value
        if value:
            CameraService.enable(self)
        else:
            CameraService.disable(self)

    @property
    def smooth_scale(self) -> bool:
        return self._smooth_scale

    @smooth_scale.setter
    def smooth_scale(self, flag: bool):
        self._smooth_scale = flag
        if flag:
            self._scale_method = pygame.transform.smoothscale
            return
        self._scale_method = pygame.transform.scale

    @property
    def zoom_level(self):
        return self._zoom_level

    def clear(self):
        CameraService.clear(self)

    def cull(self, renderable: Renderable) -> bool:
        bounds = renderable.get_bounds()
        return self.get_view_bounds().contains(bounds)

    def get_bounds(self) -> RectBounds:
        return CameraService.get_bounds(self)

    def get_view_bounds(self) -> CameraViewBounds:
        return CameraService.get_view_bounds(self)

    def render(self, delta_time, viewport: Viewport):
        CameraRenderer.render(self, viewport)

    def to_local(self, point: Transform) -> Transform:
        return CameraService.to_local(self, point)

    def to_world(self, point: Transform) -> Transform:
        return CameraService.to_world(self, point)

    def screen_to_world(self, point: Point, viewport_index: int = 0) -> Point:
        return CameraService.screen_to_world(self, point, viewport_index)

    def screen_to_world_clamped(
        self, point: Point, viewport_index: int = 0
    ) -> Point | None:
        return CameraService.screen_to_world_clamped(self, point, viewport_index)

    def zoom(self, zoom_level: float):
        CameraService.zoom(self, zoom_level)
