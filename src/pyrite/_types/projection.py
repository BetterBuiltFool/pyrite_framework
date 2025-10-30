from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygame import Rect, Vector2, Vector3
    from pygame.typing import Point


class Projection(ABC):
    """
    An object representing the parameteres of a camera's projection into the world
    space. The render system makes use of this to correctly place renderable items on
    the screen.
    """

    @property
    @abstractmethod
    def far_plane(self) -> Rect:
        """
        A Rect describing the characteristics of the projection's far plane.
        """

    @property
    @abstractmethod
    def z_near(self) -> float:
        """
        Distance of the near plane from the projection source.
        """

    @property
    @abstractmethod
    def z_far(self) -> float:
        """
        Distance of the far plane from the projection source.
        """

    @property
    @abstractmethod
    def z_depth(self) -> float:
        """
        Total depth of the projected area.
        """

    @abstractmethod
    def local_to_eye(self, local_point: Point, zoom_level: float = 1) -> Vector3:
        """
        Converts from a position in local space to the camera to the eye coordinates of
        the projection.

        :param local_point: A point in camera-local space
        :param zoom_level: The zoom level of the camera, defaults to 1
        :return: A point in 3D eye space
        """

    @abstractmethod
    def eye_to_local(self, eye_coords: Vector3, zoom_level: float = 1) -> Vector2:
        """
        Converts an eye-coordinate position to the local space of the camera.

        :param eye_coords: A point in 3D eye space
        :param zoom_level: The zoom level of the camera, defaults to 1
        :return: A point in camera-local space
        """

    @abstractmethod
    def ndc_to_eye(self, ndc_coords: Vector3) -> Vector3:
        """
        Converts Normalized Device Coordinates into eye coordinates for the projection.

        :param ndc_coords: A 3D point in NDC space.
        :return: The equivalent point in the projection's local space.
        """

    @abstractmethod
    def eye_to_ndc(self, eye_coords: Vector3) -> Vector3:
        """
        Converts a point in the projection's local space into Normalized Device
        Coordinates.

        :param eye_coords: A 3D point in the projection's local space.
        :return: The equivalent point in NDC space.
        """
