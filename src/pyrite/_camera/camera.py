from __future__ import annotations

from collections.abc import Sequence
from typing import Self, TYPE_CHECKING

import pygame

from pyrite.core.enableable import Enableable
from pyrite._camera.ortho_projection import OrthoProjection
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
        HasTransformAttributes,
    )
    from pyrite._types.projection import Projection
    from pyrite.types import CubeLike


class BaseCamera(Camera, Enableable[CameraService], manager=CameraService):
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
        transform: HasTransformAttributes | None = None,
        render_targets: RenderTarget | Sequence[RenderTarget] | None = None,
        layer_mask: Sequence[Layer] | None = None,
        enabled=True,
    ) -> None:
        super().__init__(enabled)
        if transform is not None:
            if isinstance(transform, TransformComponent):
                # If we're being passed something else's transform,
                # we'll just use that instead.
                self.transform = transform
            else:
                self.transform = TransformComponent.from_transform(self, transform)
        else:
            self.transform = TransformComponent.from_attributes(self, position)
        self._projection = projection
        self._active_projection = projection
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
        self._zoom_level: float = 1
        CameraService.add_camera(self)

        self.chaser: EntityChaser | None = None

    def __init_subclass__(cls, **kwds) -> None:
        return super().__init_subclass__(manager=CameraService, **kwds)

    @property
    def projection(self) -> Projection:
        """
        The projection used by the camera for converting items to the view space.

        Returns the zoomed version of the projection. To get the reference projection,
        use `camera._projection`.

        Setting the projection will set the reference projection, and zoom to the
        current zoom level.
        """
        return self._active_projection

    @projection.setter
    def projection(self, projection: Projection) -> None:
        self._projection = projection
        self._active_projection = self._projection.zoom(self.zoom_level)

    @property
    def zoom_level(self):
        """
        The degree to which the camera is zoomed.

        Larger number = smaller view.

        This carries over even if the projection of the camera is otherwise changed.
        """
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
        """
        Causes the camera to chase after the target.


        :param target: Any object that has a transform component.
        :param ease_factor: The rate at which the camera will try to recenter around
            the target, defaults to 8.0
        :param max_distance: The maximum distance the camera can be from the target,
            defaults to -1.0. If the target is moving too fast for the ease factor to
            keep up, the camera will be sped up to preserve this distance. -1 will
            disable.
        """
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
        """
        Stops chasing the current target, if it exists.
        """
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

    def get_mouse_position(self, viewport: Viewport | None = None) -> Transform:
        """
        Gets the current mouse position, relative to a viewport. If no viewport is
        specified, the first viewport of the camera is used.

        :param viewport: The target viewport, defaults to None
        :raises RuntimeError: If no viewport is specified, and the camera only renders
            to RenderTextures
        :return: A Transform representing the mouse position in world space.
        """
        screen_pos = pygame.mouse.get_pos()
        if not viewport:
            if len(self._viewports) < 1:
                raise RuntimeError(
                    f"{self} does not have a valid viewport and cannot see the cursor."
                    " Only cameras that render to the window can call"
                    " get_mouse_position."
                )
            viewport = self._viewports[0]
        return CameraService.screen_to_world(screen_pos, self, viewport)

    def zoom(self, zoom_level: float):
        self._active_projection = self._projection.zoom(zoom_level)
        CameraService.zoom(self, zoom_level)

    @classmethod
    def ortho(
        cls,
        cuboid: CubeLike | None = None,
        position: Point = (0, 0),
        transform: HasTransformAttributes | None = None,
        render_targets: RenderTarget | Sequence[RenderTarget] | None = None,
        layer_mask: Sequence[Layer] | None = None,
        enabled=True,
    ) -> Self:
        """
        Create a new orthographic camera.

        :param cuboid: Dimensions for the projection, None results in a camera the
            scaled to the device, defaults to None
        :param position: The starting position of the camera, in world space, defaults
            to (0, 0)
        :param transform: A Transform object or TransformComponent, used for setting up
            the new camera's TransformComponent, defaults to None. If none, a new
                component will be constructed using _position_.
        :param render_targets: A destination or sequence of destinations that the
            camera will render to, defaults to None. If None, will target the default
            viewport.
        :param layer_mask: A sequence of layers that are invisible to the camera,
            defaults to None
        :param enabled: Determines if the camera starts in a functioning state,
            defaults to True
        :return: A Camera object with an orthographic projection.
        """
        projection = OrthoProjection(cuboid)
        return cls(projection, position, transform, render_targets, layer_mask, enabled)

    @classmethod
    def perspective(
        cls,
        fov_y: float,
        aspect_ratio: float,
        z_near: float,
        z_far: float,
        position: Point = (0, 0),
        transform: HasTransformAttributes | None = None,
        render_targets: RenderTarget | Sequence[RenderTarget] | None = None,
        layer_mask: Sequence[Layer] | None = None,
        enabled=True,
    ) -> Self:
        """
        Create a new perspective camera.

        :param fov_y: Angle, in radians, of the y axis of the projection.
        :param aspect_ratio: Ratio between height and width of the view.
        :param z_near: Cut-off distance closer to the view angle. Should not be
            negative.
        :param z_far: Cut-off distance further from the view angle.
        :param position: The starting position of the camera, in world space, defaults
            to (0, 0)
        :param transform: A Transform object or TransformComponent, used for setting up
            the new camera's TransformComponent, defaults to None. If none, a new
                component will be constructed using _position_.
        :param render_targets: A destination or sequence of destinations that the
            camera will render to, defaults to None. If None, will target the default
            viewport.
        :param layer_mask: A sequence of layers that are invisible to the camera,
            defaults to None
        :param enabled: Determines if the camera starts in a functioning state,
            defaults to True
        :raises NotImplementedError: _description_
        :return: A Camera object with a perspective projection.
        """
        raise NotImplementedError("Perspective projection not yet working as intended.")
