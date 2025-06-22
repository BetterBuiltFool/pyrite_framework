from __future__ import annotations

from typing import TYPE_CHECKING
from weakref import WeakKeyDictionary

import pygame
from pygame import Surface, Vector2, Vector3

from ..rendering import RectBounds, ViewPlane
from ..transform import Transform

if TYPE_CHECKING:
    from .camera import Camera
    from ..types import CameraViewBounds, CullingBounds
    from ..rendering import Viewport
    from pygame import Rect
    from pygame.typing import Point


class CameraService:

    _surfaces: WeakKeyDictionary[Camera, Surface] = WeakKeyDictionary()
    _active_cameras: set[Camera] = set()
    _default_camera: Camera = None

    @classmethod
    def add_camera(cls, camera: Camera):
        """
        Adds the camera to the service.

        :param camera: The Camera object being added.
        """
        cls._rebuild_surface(camera)

    @classmethod
    def enable(cls, camera: Camera):
        """
        Marks a camera as being active and thus rendering.

        :param camera: The Camera object to be enabled.
        """
        cls._active_cameras.add(camera)

    @classmethod
    def disable(cls, camera: Camera):
        """
        Marks a Camera object as being inactive, and not rendering.

        :param camera: The Camera object to be disabled. Does nothing if the camera is
            already disabled.
        """
        cls._active_cameras.discard(camera)

    @classmethod
    def refresh(cls, camera: Camera):
        surface = cls._surfaces.get(camera)
        surface.fill((0, 0, 0))

    @classmethod
    def get_active_cameras(cls) -> list[Camera]:
        """
        Returns a list of all active cameras.

        :return: A list containing all enabled cameras.
        """
        return list(cls._active_cameras)

    @classmethod
    def get_render_cameras(cls) -> list[Camera]:
        """
        Returns a list containing all active cameras. If there are no active cameras, a
        default camera representing the display is supplied isntead.

        :return: A list of cameras.
        """
        return (
            list(cls._active_cameras) if cls._active_cameras else [cls._default_camera]
        )

    @classmethod
    def get_bounds(cls, camera: Camera) -> CullingBounds:
        return RectBounds(cls.get_rect(camera))

    @classmethod
    def get_rect(cls, camera: Camera) -> Rect:
        surface = cls._surfaces.get(camera)
        return surface.get_rect()

    @classmethod
    def get_view_bounds(cls, camera: Camera) -> CameraViewBounds:
        return ViewPlane(cls._get_view_rect(camera))

    @classmethod
    def _get_view_rect(cls, camera: Camera) -> Rect:
        surface = cls._surfaces.get(camera)
        surface_rect = surface.get_rect().copy()
        surface_rect.center = camera.transform.world_position
        return surface_rect

    @classmethod
    def _get_projection_data(cls, camera: Camera) -> tuple[float, ...]:
        projection = camera.projection
        far_plane = projection.far_plane
        width, height = far_plane.size
        depth = projection.z_depth
        center_x, center_y = far_plane.center
        return width, height, depth, center_x, center_y

    @classmethod
    def is_enabled(cls, camera: Camera) -> bool:
        return camera in cls._active_cameras

    @classmethod
    def local_to_ndc(cls, camera: Camera, local_coords: Vector3) -> Vector3:
        """
        Takes a point in local coordinates and transforms it into ndc space.

        :param clip_coords: A 3D point in the local space of the camera.
            For 2D, the Z axis is ignored.
        :return: A 3D point in standard ndc space.
        """
        # Frankly the only reason this is here is because the method will vary
        # depending on the renderer.
        # Default pyrite renderer doesn't use matrices, but openGL would, and I don't
        # want to have to overwrite the projection classes if it can be avoided.

        width, height, depth, center_x, center_y = cls._get_projection_data(camera)
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

    @classmethod
    def ndc_to_local(cls, camera: Camera, ndc_coords: Vector3) -> Vector3:
        """
        Takes a point in ndc space and transforms it into local coordinates

        :param ndc_coords: A 3D point in ndc space.
        :return: A 3D point in clip coordinates of the projection.
        """
        width, height, depth, center_x, center_y = cls._get_projection_data(camera)
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

    @classmethod
    def _rebuild_surface(cls, camera: Camera):
        zoom_factor = 1 / camera.zoom_level
        display_size = camera.projection.far_plane.size
        surface_size = (display_size[0] * zoom_factor), (display_size[1] * zoom_factor)
        surface = Surface(surface_size)
        cls._surfaces.update({camera: surface})

    @classmethod
    def to_local(cls, camera: Camera, point: Transform) -> Transform:
        return point.localize(camera.transform.world())

    @classmethod
    def to_eye(cls, camera: Camera, point: Transform) -> Transform:
        far_plane_center = camera.projection.far_plane.center
        far_plane_center = (
            far_plane_center[0] / camera.zoom_level,
            far_plane_center[1] / camera.zoom_level,
        )
        local_transform = Transform(
            point.position + far_plane_center, point.rotation, point.scale
        )
        return local_transform

    @classmethod
    def point_to_local(cls, camera: Camera, point: Point) -> Point:
        camera_transform = camera.transform.world()
        offset_point = Vector2(point) - camera_transform.position
        rotated_position = offset_point.rotate(camera_transform.rotation)
        new_position = rotated_position.elementwise() / camera_transform.scale

        return new_position

    @classmethod
    def local_point_to_projection(cls, camera: Camera, point: Point) -> Point:
        far_plane_center = camera.projection.far_plane.center
        far_plane_center = (
            far_plane_center[0] / camera.zoom_level,
            far_plane_center[1] / camera.zoom_level,
        )
        return point + far_plane_center

    @classmethod
    def to_world(cls, camera: Camera, point: Transform) -> Transform:
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

    @classmethod
    def screen_to_world(
        cls, camera: Camera, point: Point, viewport_index: int = 0
    ) -> Point:
        # TODO Implement this
        # viewport = self.viewports[viewport_index]
        # viewport_rect = self._get_viewport_rect(viewport)

        # viewport_world = self.get_viewport_rect()

        # viewport_space_position = self._screen_to_viewport(
        #     point, viewport_rect, Vector2(viewport_world.size)
        # )

        # return viewport_space_position.elementwise() + viewport_world.topleft
        pass

    @classmethod
    def screen_to_world_clamped(
        cls, camera: Camera, point: Point, viewport_index: int = 0
    ) -> Point | None:
        # TODO Implement this
        # viewport = self.viewports[viewport_index]
        # viewport_rect = self._get_viewport_rect(viewport)

        # if not viewport_rect.collidepoint(point):
        #     return None

        # viewport_world = self.get_viewport_rect()

        # viewport_space_position = self._screen_to_viewport(
        #     point, viewport_rect, Vector2(viewport_world.size)
        # )

        # return viewport_space_position.elementwise() + viewport_world.topleft
        pass

    @classmethod
    def world_to_screen(cls, point: Point, camera: Camera, viewport: Viewport) -> Point:
        local_coords = cls.point_to_local(camera, point)
        if viewport.crop:
            coords = viewport.local_to_screen(local_coords)
        else:
            eye_coords = cls.local_point_to_projection(camera, local_coords)
            ndc_coords = cls.local_to_ndc(camera, Vector3(*eye_coords, 0))
            coords = viewport.ndc_to_screen(ndc_coords)
        return coords

    @classmethod
    def update_default_camera(cls, size: Point):
        """
        Updates the default camera so its projection matches the size of the display.

        :param size: A point representing the size of the display
        """
        # Update the camera surface so we can draw on it correctly.
        cls._surfaces.update({cls._default_camera: pygame.display.get_surface()})

    @classmethod
    def zoom(cls, camera: Camera, zoom: float):
        camera._zoom_level = zoom
        cls._rebuild_surface(camera)
