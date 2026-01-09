from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygame import Rect

    import glm


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
    def zoom(self, zoom_factor: float) -> Projection:
        """
        Returns a new projection with the same characteristics as the current one, as
        if zoomed in by the given degree.

        :param zoom_factor: The degree of zooming performed
        :return: The new, zoomed projection.
        """
