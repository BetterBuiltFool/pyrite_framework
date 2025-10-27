from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

import pygame
from pygame import Vector2

from pyrite._services.camera_service import CameraServiceProvider as CameraService
from pyrite._entity.entity_chaser import EntityChaser
from pyrite.enum import Layer
from pyrite.events import OnEnable, OnDisable
from pyrite._rendering.camera_renderer import CameraRendererProvider as CameraRenderer
from pyrite._rendering.viewport import Viewport
from pyrite._component.transform_component import TransformComponent
from pyrite._transform.transform import Transform
from pyrite._types.camera import Camera
from pyrite._types.renderable import Renderable

if TYPE_CHECKING:
    from pygame.typing import Point

    from pyrite._types.view_bounds import CameraViewBounds
    from pyrite._types.protocols import (
        HasTransform,
        HasTransformProperty,
        RenderTarget,
        TransformLike,
    )
    from pyrite._types.projection import Projection


class BaseCamera(Camera):
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

        self.chaser: EntityChaser | None = None

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

    def chase(
        self,
        target: HasTransform | HasTransformProperty,
        ease_factor: float = 8.0,
        max_distance: float = -1.0,
    ) -> None:
        if self.chaser:
            self.chaser.stop()
        self.chaser = EntityChaser(
            transform=self.transform,
            position=self.transform.world_position,
            target=target,
            ease_factor=ease_factor,
            max_distance=max_distance,
            dist_function=self._clamp_distance,
        )

    def stop_chase(self) -> None:
        if self.chaser:
            self.chaser.stop()
        self.chaser = None

    def _clamp_distance(self, distance: float) -> float:
        return distance / self.zoom_level

    def cull(self, renderable: Renderable) -> bool:
        bounds = renderable.get_bounds()
        return self.get_view_bounds().contains(bounds)

    def get_view_bounds(self) -> CameraViewBounds:
        return CameraService.get_view_bounds(self)

    def get_viewports(self) -> list[Viewport]:
        return self._viewports

    def render(self, render_target: RenderTarget):
        CameraRenderer.render(self, render_target)

    def to_local(self, point: Transform) -> Transform:
        return CameraService.to_local(self, point)

    def to_eye(self, point: Transform) -> Transform:
        return CameraService.to_eye(self, point)

    def to_world(self, point: Transform) -> Transform:
        return CameraService.to_world(self, point)

    def get_mouse_position(self, viewport: Viewport | None = None) -> Vector2:
        screen_pos = pygame.mouse.get_pos()
        if not viewport:
            if len(self._viewports) < 1:
                raise RuntimeError(
                    f"{self} does not have a valid viewport and cannot see the cursor."
                    " Only cameras that render to the window can call"
                    " get_mouse_position."
                )
            viewport = self._viewports[0]
        return self._get_mouse_position(viewport, screen_pos)

    def _get_mouse_position(self, viewport: Viewport, screen_pos: Point) -> Vector2:
        ndc_coords = viewport.screen_to_ndc(screen_pos)
        eye_coords = self.projection.ndc_to_eye(ndc_coords)
        return CameraService.from_eye(self, Transform(eye_coords.xy)).position

    # def screen_to_world(self, point: Point, viewport_index: int = 0) -> Point:
    #     return CameraService.screen_to_world(self, point, viewport_index)

    # def screen_to_world_clamped(
    #     self, point: Point, viewport_index: int = 0
    # ) -> Point | None:
    #     return CameraService.screen_to_world_clamped(self, point, viewport_index)

    def zoom(self, zoom_level: float):
        CameraService.zoom(self, zoom_level)
