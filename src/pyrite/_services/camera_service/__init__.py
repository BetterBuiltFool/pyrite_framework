from __future__ import annotations

from typing import TYPE_CHECKING

from pyrite._types.service import ServiceProvider
from pyrite._services.camera_service.camera_service import (
    CameraService,
    DefaultCameraService,
)

if TYPE_CHECKING:
    from pygame.typing import Point
    from pygame import Vector3

    from pyrite._transform.transform import Transform
    from pyrite._types.camera import Camera
    from pyrite._types.view_bounds import CameraViewBounds
    from pyrite._rendering.viewport import Viewport


class CameraServiceProvider(ServiceProvider[CameraService]):
    """
    Service that contains and maintains data for Camera objects.
    """

    _service: CameraService = DefaultCameraService()
    _active_cameras: set[Camera] = set()
    _default_camera: Camera

    @classmethod
    def hotswap(cls, service: CameraService):
        cls._service.transfer(service)
        cls._service = service

    # -----------------------CameraService Specific-----------------------

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
    def is_enabled(cls, camera: Camera) -> bool:
        """
        Tells if the given camera is currently enabled.

        :param camera: A Camera object of unknown status.
        :return: True if the camera is currently active, otherwise False
        """
        return camera in cls._active_cameras

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
        Returns a list containing all active cameras. If there are no active cameras
        drawing to a viewport, a default camera representing the display is supplied
        instead.

        :return: A list of cameras.
        """
        return (
            list(cls._active_cameras) if cls._active_cameras else [cls._default_camera]
        )

    # -----------------------Delegates-----------------------

    @classmethod
    def add_camera(cls, camera: Camera):
        """
        Adds the camera to the service.

        :param camera: The Camera object being added.
        """
        cls._service.add_camera(camera)

    @classmethod
    def refresh(cls, camera: Camera):
        """
        Updates the camera's cached data at the beginning of a new frame.

        :param camera: The Camera object being refreshed.
        """
        cls._service.refresh(camera)

    @classmethod
    def get_view_bounds(cls, camera: Camera) -> CameraViewBounds:
        """
        Returns the viewable area of the given camera.

        :param camera: A Camera object whose viewing bounds are required.
        :return: The viewing bounds of the camera.
        """
        return cls._service.get_view_bounds(camera)

    @classmethod
    def local_to_ndc(cls, camera: Camera, local_coords: Vector3) -> Vector3:
        """
        Takes a point in local coordinates and transforms it into ndc space.

        :param clip_coords: A 3D point in the local space of the camera.
            For 2D, the Z axis is ignored.
        :return: A 3D point in standard ndc space.
        """
        return cls._service.local_to_ndc(camera, local_coords)

    @classmethod
    def ndc_to_local(cls, camera: Camera, ndc_coords: Vector3) -> Vector3:
        """
        Takes a point in ndc space and transforms it into local coordinates

        :param ndc_coords: A 3D point in ndc space.
        :return: A 3D point in clip coordinates of the projection.
        """
        return cls._service.ndc_to_local(camera, ndc_coords)

    @classmethod
    def to_local(cls, camera: Camera, point: Transform) -> Transform:
        """
        Converts the transform into the local space of the camera.

        :param camera: A Camera object whose local space is being considered.
        :param point: A Transform, in world space, being converted to the local space
            of the camera.
        :return: A Transform representing the point, as relative to the camera.
        """
        return cls._service.to_local(camera, point)

    @classmethod
    def to_eye(cls, camera: Camera, point: Transform) -> Transform:
        """
        Converts a transform local to the camera into the eye coordinates of the
        camera's projection.

        :param camera: The Camera object, which the point is local to.
        :param point: A Transform local to the camera.
        :return: A Transform from _point_, as it exists relative to the projection.
        """
        return cls._service.to_eye(camera, point)

    @classmethod
    def point_to_local(cls, camera: Camera, point: Point) -> Point:
        """
        Converts a point in world space to the local space of the camera, without the
        baggage of a Transform.

        :param camera: The Camera object, whose space is being converted to.
        :param point: A point in world space. Position only.
        :return: A point, as it exists relative to the camera.
        """
        return cls._service.point_to_local(camera, point)

    @classmethod
    def local_point_to_projection(cls, camera: Camera, point: Point) -> Point:
        """
        Converts a point in space local to the camera to the projection space of the
        camera, without the baggage of a Transform.

        :param camera: The Camera object, which the point is local to.
        :param point: A point local to the camera. Position only.
        :return: A point, as it exists relative to the projection.
        """
        return cls._service.local_point_to_projection(camera, point)

    @classmethod
    def from_eye(cls, camera: Camera, point: Transform) -> Transform:
        """
        Converts a transform from eye-space coordinates to local space of the camera.

        :param camera: The Camera object, which the point is being made relative to.
        :param point: A Transform in the eye space of the camera.
        :return: A Transform in the local space of the camera.
        """
        return cls._service.from_eye(camera, point)

    @classmethod
    def to_world(cls, camera: Camera, point: Transform) -> Transform:
        """
        Converts a point local to the camera to its world space equivalent.

        :param camera: The Camera object, which the point is local to.
        :param point: A Transform representing a local space to the camera.
        :return: A Transform in the world space.
        """
        return cls._service.to_world(camera, point)

    @classmethod
    def world_to_screen(cls, point: Point, camera: Camera, viewport: Viewport) -> Point:
        """
        Converts the given point into screen space for the given camera and viewport.

        :param point: A point, in world space.
        :param camera: A Camera object, whose view is being considered.
        :param viewport: The viewport to specify which portion of the screen is being
            referenced.
        :return: A point in screen space.
        """
        return cls._service.world_to_screen(point, camera, viewport)

    @classmethod
    def update_default_camera(cls, size: Point):
        """
        Returns the viewable area of the given camera.

        :param camera: A Camera object whose viewing bounds are required.
        :return: The viewing bounds of the camera.
        """
        cls._service.update_default_camera(cls._default_camera, size)

    @classmethod
    def zoom(cls, camera: Camera, zoom: float):
        """
        Updates the zoom level of the camera, so the camera appears zoomed in or out.

        :param camera: The Camera object whose zoom is being altered.
        :param zoom: The new level of zoom for the camera.
        """
        cls._service.zoom(camera, zoom)
