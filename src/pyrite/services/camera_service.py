from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from weakref import WeakKeyDictionary

import pygame
from pygame import Surface, Vector2, Vector3

from ..rendering import RectBounds, ViewPlane
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
