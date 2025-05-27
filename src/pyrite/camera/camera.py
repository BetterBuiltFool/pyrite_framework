from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, TypeVar

from .camera_service import CameraService
from .default_camera import DefaultCamera
from ..rendering.viewport import Viewport
from ..enum import Layer, RenderLayers
from ..rendering.camera_renderer import CameraRenderer
from ..rendering.rect_bounds import RectBounds
from ..transform import transform_component
from ..types import Renderable

import pygame
from pygame import Vector2

if TYPE_CHECKING:
    from ..types import CameraViewBounds, Container, CameraBase, TransformProtocol
    from ..types.projection import Projection
    from pygame.typing import Point
    from pygame import Surface

    P = TypeVar("P", bound=Projection)


class Camera(DefaultCamera, Renderable):

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
            viewports = [Viewport()]
        if not isinstance(viewports, Sequence):
            viewports = [viewports]
        self.viewports: Sequence[Viewport] = viewports
        DefaultCamera.__init__(self, surface=None, layer_mask=layer_mask)
        Renderable.__init__(
            self,
            container=container,
            enabled=enabled,
            layer=RenderLayers.CAMERA,
            draw_index=draw_index,
        )
        self._zoom_level = 1
        CameraService.add_camera(self)

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

    def draw_to_view(self, surface: Surface, position: Point):
        CameraService.draw_to_camera(self, surface, position)

    def get_bounds(self) -> RectBounds:
        return CameraService.get_bounds(self)

    def get_view_bounds(self) -> CameraViewBounds:
        return CameraService.get_view_bounds(self)

    def render(self, delta_time: float, camera: CameraBase):
        CameraRenderer.render(self, camera)

    def to_local(self, point: Point) -> Point:
        return CameraService.to_local(self, point)

    def to_world(self, point: Point) -> Vector2:
        return CameraService.to_world(self, point)

    def screen_to_world(self, point: Point, viewport_index: int = 0) -> Point:
        return CameraService.screen_to_world(self, point, viewport_index)

    def screen_to_world_clamped(
        self, point: Point, viewport_index: int = 0
    ) -> Point | None:
        return CameraService.screen_to_world_clamped(self, point, viewport_index)

    def scale_view(
        self, camera_surface: pygame.Surface, target_size: Point
    ) -> pygame.Surface:
        """
        Returns a scaled version of the camera's view surface using the camera's chosen
        scale method.

        :param camera_surface: the rendered camera surface
        :param target_size: Destination size of the surface
        :return: The scaled surface.
        """
        return self._scale_method(camera_surface, target_size)

    def zoom(self, zoom_level: float):
        CameraService.zoom(self, zoom_level)
