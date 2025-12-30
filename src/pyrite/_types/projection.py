from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygame import Rect

    import glm

    from pyrite._transform.transform import Transform
    from pyrite._types.protocols import HasTransformAttributes


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
    def get_matrix(self) -> glm.mat4x4:
        """
        Generates a projection matrix based on the projection data.
        """

    @abstractmethod
    def local_to_eye(self, local_coords: HasTransformAttributes) -> Transform:
        """
        Converts from a position in local space to the camera to the eye coordinates of
        the projection.

        :param local_coords: A point in camera-local space
        :return: A point in 3D eye space
        """

    @abstractmethod
    def eye_to_local(self, eye_coords: HasTransformAttributes) -> Transform:
        """
        Converts an eye-coordinate position to the local space of the camera.

        :param eye_coords: A point in 3D eye space
        :return: A point in camera-local space
        """

    @abstractmethod
    def ndc_to_eye(self, ndc_coords: HasTransformAttributes) -> Transform:
        """
        Converts Normalized Device Coordinates into eye coordinates for the projection.

        :param ndc_coords: A 3D point in NDC space.
        :return: The equivalent point in the projection's local space.
        """

    @abstractmethod
    def eye_to_ndc(self, eye_coords: HasTransformAttributes) -> Transform:
        """
        Converts a point in the projection's local space into Normalized Device
        Coordinates.

        :param eye_coords: A 3D point in the projection's local space.
        :return: The equivalent point in NDC space.
        """

    @abstractmethod
    def zoom(self, zoom_factor: float) -> Projection:
        """
        Returns a new projection with the same characteristics as the current one, as
        if zoomed in by the given degree.

        :param zoom_factor: The degree of zooming performed
        :return: The new, zoomed projection.
        """
