from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

import glm
from weakref import WeakKeyDictionary

from pygame import Surface

from pyrite._rendering.view_plane import ViewPlane
from pyrite._types.service import Service
from pyrite._transform.transform import Transform

if TYPE_CHECKING:
    from pygame import Rect
    from pygame.typing import Point
    from pyrite._types.camera import Camera
    from pyrite._types.view_bounds import CameraViewBounds
    from pyrite._rendering.viewport import Viewport


class CameraService(Service):

    @abstractmethod
    def add_camera(self, camera: Camera):
        pass

    @abstractmethod
    def refresh(self, camera: Camera):
        pass

    @abstractmethod
    def get_view_bounds(self, camera: Camera) -> CameraViewBounds:
        pass

    @abstractmethod
    def world_to_clip(self, camera: Camera, world_coords: Transform) -> Transform:
        pass

    @abstractmethod
    def clip_to_world(self, camera: Camera, clip_coords: Transform) -> Transform:
        pass

    @abstractmethod
    def world_to_screen(
        self, point: Point, camera: Camera, viewport: Viewport
    ) -> Point:
        pass

    @abstractmethod
    def screen_to_world(
        self, point: Point, camera: Camera, viewport: Viewport
    ) -> Transform:
        pass

    @abstractmethod
    def update_default_camera(self, default_camera: Camera, size: Point):
        pass

    @abstractmethod
    def zoom(self, camera: Camera, zoom: float):
        pass


class DefaultCameraService(CameraService):

    def __init__(self) -> None:
        self._surfaces: WeakKeyDictionary[Camera, Surface] = WeakKeyDictionary()
        self._projections: WeakKeyDictionary[Camera, glm.mat4x4] = WeakKeyDictionary()
        self._invert_projections: WeakKeyDictionary[Camera, glm.mat4x4] = (
            WeakKeyDictionary()
        )

    def transfer(self, target_service: CameraService):
        for camera in self._surfaces:
            target_service.add_camera(camera)

    def _update_projection_matrix(self, camera: Camera) -> None:
        projection = self._premult_matrix(
            camera.projection.get_matrix(),
            camera.transform.world().matrix,
        )
        self._projections[camera] = projection
        self._invert_projections[camera] = glm.inverse(projection)

    def _premult_matrix(
        self, projection: glm.mat4x4, view_matrix: glm.mat4x4
    ) -> glm.mat4x4:
        return projection * glm.inverse(view_matrix)

    def _premult_invert(
        self, projection: glm.mat4x4, view_matrix: glm.mat4x4
    ) -> glm.mat4x4:
        return glm.inverse(projection) * view_matrix

    def add_camera(self, camera: Camera):
        self._update_projection_matrix(camera)
        return self._rebuild_surface(camera)

    def refresh(self, camera: Camera):
        surface = self._surfaces[camera]
        surface.fill((0, 0, 0, 0))
        self._update_projection_matrix(camera)

    def get_view_bounds(self, camera: Camera) -> CameraViewBounds:
        return ViewPlane(self._get_view_rect(camera))

    def _get_view_rect(self, camera: Camera) -> Rect:
        surface = self._surfaces[camera]
        surface_rect = surface.get_rect().copy()
        surface_rect.center = camera.transform.world_position
        return surface_rect

    def world_to_clip(self, camera: Camera, world_coords: Transform) -> Transform:
        projection = self._projections[camera]
        return Transform.from_matrix(projection * world_coords)

    def clip_to_world(self, camera: Camera, clip_coords: Transform) -> Transform:
        projection = self._invert_projections[camera]
        world_coords = Transform.from_matrix(projection * clip_coords)
        # projection inversion messes up the scaling, so we reset it here.
        world_coords.scale = (1, 1)
        return world_coords

    def _rebuild_surface(self, camera: Camera):
        display_size = camera.projection.far_plane.size
        self._surfaces[camera] = Surface(display_size)

    def world_to_screen(
        self, point: Point, camera: Camera, viewport: Viewport
    ) -> Point:
        world_coords = Transform.from_2d(point)
        ndc_coords = self.world_to_clip(camera, world_coords)
        return viewport.clip_to_viewport(ndc_coords)

    def screen_to_world(
        self, point: Point, camera: Camera, viewport: Viewport
    ) -> Transform:
        clip_coords = viewport.viewport_to_clip(point)
        return self.clip_to_world(camera, clip_coords)

    def update_default_camera(self, default_camera: Camera, size: Point):
        self._surfaces[default_camera] = Surface(size)

    def zoom(self, camera: Camera, zoom: float):
        camera.zoom_level = zoom
        self._rebuild_surface(camera)
