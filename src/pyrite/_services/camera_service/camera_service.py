from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from weakref import WeakKeyDictionary

from pygame import Surface, Vector2, Vector3

from pyrite._rendering.view_plane import ViewPlane
from pyrite._types.service import Service

if TYPE_CHECKING:
    from pygame import Rect
    from pygame.typing import Point
    from pyrite._types.camera import CameraBase as Camera
    from pyrite._transform.transform import Transform
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
    def point_to_local(self, camera: Camera, point: Point) -> Point:
        pass

    @abstractmethod
    def local_point_to_projection(self, camera: Camera, point: Point) -> Point:
        pass

    @abstractmethod
    def from_eye(self, camera: Camera, point: Transform) -> Transform:
        pass

    @abstractmethod
    def to_world(self, camera: Camera, point: Transform) -> Transform:
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

    def transfer(self, target_service: CameraService):
        for camera in self._surfaces:
            target_service.add_camera(camera)

    def add_camera(self, camera: Camera):
        return self._rebuild_surface(camera)

    def refresh(self, camera: Camera):
        surface = self._surfaces[camera]
        surface.fill((0, 0, 0, 0))

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

    def local_to_ndc(self, camera: Camera, local_coords: Vector3) -> Vector3:

        width, height, depth, center_x, center_y = self._get_projection_data(camera)
        # Convert the local coords to projection space center.
        zoom_level = camera.zoom_level
        eye_point = (
            (local_coords.x * zoom_level) - center_x,
            (local_coords.y * zoom_level) - center_y,
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
        zoom_level = camera.zoom_level
        local_coords = Vector3(
            center_x + projection_coords[0] / zoom_level,
            center_y + projection_coords[1] / zoom_level,
            projection_coords[2],
        )
        return local_coords

    def _rebuild_surface(self, camera: Camera):
        zoom_factor = 1 / camera.zoom_level
        display_size = camera.projection.far_plane.size
        surface_size = (display_size[0] * zoom_factor), (display_size[1] * zoom_factor)
        surface = Surface(surface_size)
        self._surfaces[camera] = surface

    def to_local(self, camera: Camera, point: Transform) -> Transform:
        return point.localize(point, camera.transform.world())

    def to_eye(self, camera: Camera, point: Transform) -> Transform:
        far_plane_center = camera.projection.far_plane.center
        far_plane_center = (
            far_plane_center[0] / camera.zoom_level,
            far_plane_center[1] / camera.zoom_level,
        )
        local_transform = point.copy()
        local_transform.position = point.position + far_plane_center
        return local_transform

    def point_to_local(self, camera: Camera, point: Point) -> Point:
        camera_transform = camera.transform.world()
        offset_point = Vector2(point) - camera_transform.position
        rotated_position = offset_point.rotate(camera_transform.rotation)
        new_position = rotated_position.elementwise() / camera_transform.scale

        return new_position

    def local_point_to_projection(self, camera: Camera, point: Point) -> Point:
        far_plane_center = camera.projection.far_plane.center
        far_plane_center = (
            far_plane_center[0] / camera.zoom_level,
            far_plane_center[1] / camera.zoom_level,
        )
        return point[0] + far_plane_center[0], point[1] + far_plane_center[1]

    def from_eye(self, camera: Camera, point: Transform) -> Transform:
        # TODO Implement
        return super().from_eye(camera, point)

    def to_world(self, camera: Camera, point: Transform) -> Transform:
        # Mkae a copy of point to avoid mutation
        point = point.copy()
        # Find the adjusted center of the camera's far plane
        far_plane_center = camera.projection.far_plane.center
        far_plane_center = (
            far_plane_center[0] / camera.zoom_level,
            far_plane_center[1] / camera.zoom_level,
        )
        # Apply the offset to return center to origin
        point.position -= far_plane_center
        # Generalize to world coords
        return point.generalize(point, camera.transform.world())

    def world_to_screen(
        self, point: Point, camera: Camera, viewport: Viewport
    ) -> Point:
        local_coords = self.point_to_local(camera, point)
        if viewport.crop:
            coords = viewport.local_to_screen(local_coords)
        else:
            eye_coords = self.local_point_to_projection(camera, local_coords)
            ndc_coords = self.local_to_ndc(
                camera, Vector3(eye_coords[0], eye_coords[1], 0)
            )
            coords = viewport.ndc_to_screen(ndc_coords)
        return coords

    def update_default_camera(self, default_camera: Camera, size: Point):
        self._surfaces[default_camera] = Surface(size)

    def zoom(self, camera: Camera, zoom: float):
        camera.zoom_level = zoom
        self._rebuild_surface(camera)
