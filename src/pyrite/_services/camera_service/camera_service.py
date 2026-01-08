from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

import glm
from weakref import WeakKeyDictionary

from pygame import Surface, Vector3

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
    def local_to_ndc(self, camera: Camera, local_coords: Vector3) -> Vector3:
        pass

    @abstractmethod
    def ndc_to_local(self, camera: Camera, ndc_coords: Vector3) -> Vector3:
        pass

    @abstractmethod
    def to_local(self, camera: Camera, point: Transform) -> Transform:
        pass

    @abstractmethod
    def to_eye(self, camera: Camera, point: Transform) -> Transform:
        pass

    @abstractmethod
    def from_eye(self, camera: Camera, point: Transform) -> Transform:
        pass

    @abstractmethod
    def to_world(self, camera: Camera, point: Transform) -> Transform:
        pass

    @abstractmethod
    def world_to_clip(self, camera: Camera, world_coords: Transform) -> Transform:
        pass

    @abstractmethod
    def world_to_screen(
        self, point: Point, camera: Camera, viewport: Viewport
    ) -> Point:
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

    def transfer(self, target_service: CameraService):
        for camera in self._surfaces:
            target_service.add_camera(camera)

    def _update_projection_matrix(self, camera: Camera) -> None:
        self._projections[camera] = self._premult_matrix(
            camera.projection.get_matrix(),
            camera.transform.world().matrix,
        )

    def _premult_matrix(
        self, projection: glm.mat4x4, view_matrix: glm.mat4x4
    ) -> glm.mat4x4:
        return projection * glm.inverse(view_matrix)
        # return projection * view_matrix

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

    def _get_projection_data(self, camera: Camera) -> tuple[float, ...]:
        projection = camera.projection
        far_plane = projection.far_plane
        width, height = far_plane.size
        depth = projection.z_depth
        center_x, center_y = far_plane.center
        return width, height, depth, center_x, center_y

    def world_to_clip(self, camera: Camera, world_coords: Transform) -> Transform:
        projection = self._projections[camera]
        return Transform.from_matrix(projection * world_coords)

    def local_to_ndc(self, camera: Camera, local_coords: Vector3) -> Vector3:

        width, height, depth, center_x, center_y = self._get_projection_data(camera)
        # Convert the local coords to projection space center.
        eye_point = (
            (local_coords.x) - center_x,
            (local_coords.y) - center_y,
            local_coords.z,
        )
        # Divide by projection size to normalize.
        ndc_coords = Vector3(
            eye_point[0] / (width / 2),
            eye_point[1] / (height / 2),
            eye_point[2] / (depth / 2),
        )
        return ndc_coords

    def ndc_to_local(self, camera: Camera, ndc_coords: Vector3) -> Vector3:
        width, height, depth, center_x, center_y = self._get_projection_data(camera)
        # Convert into projection space coords
        projection_coords = (
            int(ndc_coords[0] * (width / 2)),
            int(ndc_coords[1] * (height / 2)),
            int(ndc_coords[2] * (depth / 2)),
        )
        # Translate to local camera space.
        local_coords = Vector3(
            center_x + projection_coords[0],
            center_y + projection_coords[1],
            projection_coords[2],
        )
        return local_coords

    def _rebuild_surface(self, camera: Camera):
        display_size = camera.projection.far_plane.size
        self._surfaces[camera] = Surface(display_size)

    def to_local(self, camera: Camera, point: Transform) -> Transform:
        return Transform.new(point.localize(point, camera.transform.world()))

    def to_eye(self, camera: Camera, point: Transform) -> Transform:
        projection = self._projections[camera]
        return Transform.from_matrix(projection * point)  # type:ignore

    def from_eye(self, camera: Camera, point: Transform) -> Transform:
        return camera.projection.eye_to_local(point)

    def to_world(self, camera: Camera, point: Transform) -> Transform:
        return Transform.new(point.generalize(point, camera.transform.world()))

    def world_to_screen(
        self, point: Point, camera: Camera, viewport: Viewport
    ) -> Point:
        world_coords = Transform.from_2d(point)
        ndc_coords = self.world_to_clip(camera, world_coords)
        return viewport.ndc_to_screen(ndc_coords)

    def update_default_camera(self, default_camera: Camera, size: Point):
        self._surfaces[default_camera] = Surface(size)

    def zoom(self, camera: Camera, zoom: float):
        camera.zoom_level = zoom
        self._rebuild_surface(camera)
