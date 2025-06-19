from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from weakref import WeakKeyDictionary

import pygame
from pygame import Surface, Vector2, Vector3

from ..rendering import ViewPlane
from ..transform import Transform
from ..types.service import Service

if TYPE_CHECKING:
    from ..camera import Camera
    from ..types import CameraViewBounds
    from ..rendering import Viewport
    from pygame import Rect
    from pygame.typing import Point


class CameraService(Service):

    @abstractmethod
    def add_camera(self, camera: Camera):
        """
        Adds the camera to the service.

        :param camera: The Camera object being added.
        """

    @abstractmethod
    def enable(self, camera: Camera):
        """
        Marks a camera as being active and thus rendering.

        :param camera: The Camera object to be enabled.
        """

    @abstractmethod
    def disable(self, camera: Camera):
        """
        Marks a Camera object as being inactive, and not rendering.

        :param camera: The Camera object to be disabled. Does nothing if the camera is
            already disabled.
        """

    @abstractmethod
    def refresh(self, camera: Camera):
        """
        Updates the camera's cached data at the beginning of a new frame.

        :param camera: The Camera object being refreshed.
        """

    @abstractmethod
    def get_active_cameras(self) -> list[Camera]:
        """
        Returns a list of all active cameras.

        :return: A list containing all enabled cameras.
        """

    @abstractmethod
    def get_render_cameras(self) -> list[Camera]:
        """
        Returns a list containing all active cameras. If there are no active cameras
        drawing to a viewport, a default camera representing the display is supplied
        instead.

        :return: A list of cameras.
        """

    @abstractmethod
    def get_view_bounds(self, camera: Camera) -> CameraViewBounds:
        """
        Returns the viewable area of the given camera.

        :param camera: A Camera object whose viewing bounds are required.
        :return: The viewing bounds of the camera.
        """

    @abstractmethod
    def is_enabled(self, camera: Camera) -> bool:
        """
        Tells if the given camera is currently enabled.

        :param camera: A Camera object of unknown status.
        :return: True if the camera is currently active, otherwise False
        """

    @abstractmethod
    def local_to_ndc(self, camera: Camera, local_coords: Vector3) -> Vector3:
        """
        Takes a point in local coordinates and transforms it into ndc space.

        :param clip_coords: A 3D point in the local space of the camera.
            For 2D, the Z axis is ignored.
        :return: A 3D point in standard ndc space.
        """

    @abstractmethod
    def ndc_to_local(self, camera: Camera, ndc_coords: Vector3) -> Vector3:
        """
        Takes a point in ndc space and transforms it into local coordinates

        :param ndc_coords: A 3D point in ndc space.
        :return: A 3D point in clip coordinates of the projection.
        """

    @abstractmethod
    def to_local(self, camera: Camera, point: Transform) -> Transform:
        """
        Converts the transform into the local space of the camera.

        :param camera: A Camera object whose local space is being considered.
        :param point: A Transform, in world space, being converted to the local space
            of the camera.
        :return: A Transform representing the point, as relative to the camera.
        """

    @abstractmethod
    def to_eye(self, camera: Camera, point: Transform) -> Transform:
        """
        Converts a transform local to the camera into the eye coordinates of the
        camera's projection.

        :param camera: The Camera object, which the point is local to.
        :param point: A Transform local to the camera.
        :return: A Transform from _point_, as it exists relative to the projection.
        """

    @abstractmethod
    def point_to_local(self, camera: Camera, point: Point) -> Point:
        """
        Converts a point in world space to the local space of the camera, without the
        baggage of a Transform.

        :param camera: The Camera object, whose space is being converted to.
        :param point: A point in world space. Position only.
        :return: A point, as it exists relative to the camera.
        """

    @abstractmethod
    def local_point_to_projection(self, camera: Camera, point: Point) -> Point:
        """
        Converts a point in space local to the camera to the projection space of the
        camera, without the baggage of a Transform.

        :param camera: The Camera object, which the point is local to.
        :param point: A point local to the camera. Position only.
        :return: A point, as it exists relative to the projection.
        """

    @abstractmethod
    def from_eye(self, camera: Camera, point: Transform) -> Transform:
        """
        Converts a transform from eye-space coordinates to local space of the camera.

        :param camera: The Camera object, which the point is being made relative to.
        :param point: A Transform in the eye space of the camera.
        :return: A Transform in the local space of the camera.
        """

    @abstractmethod
    def to_world(self, camera: Camera, point: Transform) -> Transform:
        """
        Converts a point local to the camera to its world space equivalent.

        :param camera: The Camera object, which the point is local to.
        :param point: A Transform representing a local space to the camera.
        :return: A Transform in the world space.
        """

    @abstractmethod
    def world_to_screen(
        self, point: Point, camera: Camera, viewport: Viewport
    ) -> Point:
        """
        Converts the given point into screen space for the given camera and viewport.

        :param point: A point, in world space.
        :param camera: A Camera object, whose view is being considered.
        :param viewport: The viewport to specify which portion of the screen is being
            referenced.
        :return: A point in screen space.
        """

    @abstractmethod
    def update_default_camera(self, size: Point):
        """
        Forces the default camera to have a projection matching the size.

        :param size: A point describing the current size of the display.
        """

    @abstractmethod
    def zoom(self, camera: Camera, zoom: float):
        """
        Updates the zoom level of the camera, so the camera appears zoomed in or out.

        :param camera: _description_
        :param zoom: _description_
        :return: _description_
        """


class DefaultCameraService(CameraService):

    def __init__(self) -> None:
        self._surfaces: WeakKeyDictionary[Camera, Surface] = WeakKeyDictionary()
        self._active_cameras: set[Camera] = set()
        self._default_camera: Camera = None

    def transfer(self, target_service: CameraService):
        for camera in self._active_cameras:
            target_service.add_camera(camera)
        target_service.update_default_camera(
            self._default_camera.projection.far_plane.size()
        )

    def add_camera(self, camera: Camera):
        return self._rebuild_surface(camera)

    def enable(self, camera: Camera):
        self._active_cameras.add(camera)

    def disable(self, camera: Camera):
        self._active_cameras.discard(camera)

    def refresh(self, camera: Camera):
        surface = self._surfaces.get(camera)
        surface.fill((0, 0, 0, 0))

    def get_active_cameras(self) -> list[Camera]:
        return list(self._active_cameras)

    def get_render_cameras(self) -> list[Camera]:
        return (
            list(self._active_cameras)
            if self._active_cameras
            else [self._default_camera]
        )

    def get_view_bounds(self, camera: Camera) -> CameraViewBounds:
        return ViewPlane(self._get_view_rect(camera))

    def _get_view_rect(self, camera: Camera) -> Rect:
        surface = self._surfaces.get(camera)
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

    def is_enabled(self, camera: Camera) -> bool:
        return camera in self._active_cameras

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
        self._surfaces.update({camera: surface})

    def to_local(self, camera: Camera, point: Transform) -> Transform:
        return point.localize(camera.transform.world())

    def to_eye(self, camera: Camera, point: Transform) -> Transform:
        far_plane_center = camera.projection.far_plane.center
        far_plane_center = (
            far_plane_center[0] / camera.zoom_level,
            far_plane_center[1] / camera.zoom_level,
        )
        local_transform = Transform(
            point.position + far_plane_center, point.rotation, point.scale
        )
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
        return point + far_plane_center

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
        return point.generalize(camera.transform.world())

    def world_to_screen(
        self, point: Point, camera: Camera, viewport: Viewport
    ) -> Point:
        local_coords = self.point_to_local(camera, point)
        if viewport.crop:
            coords = viewport.local_to_screen(local_coords)
        else:
            eye_coords = self.local_point_to_projection(camera, local_coords)
            ndc_coords = self.local_to_ndc(camera, Vector3(*eye_coords, 0))
            coords = viewport.ndc_to_screen(ndc_coords)
        return coords

    def update_default_camera(self, size: Point):
        # Update the camera surface so we can draw on it correctly.
        # TODO Update camera's projection to match _size_
        self._surfaces.update({self._default_camera: pygame.display.get_surface()})

    def zoom(self, camera: Camera, zoom: float):
        camera._zoom_level = zoom
        self._rebuild_surface(camera)
