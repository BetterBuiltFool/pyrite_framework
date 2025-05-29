from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygame import Rect, Vector3


class Projection(ABC):

    @property
    @abstractmethod
    def far_plane(self) -> Rect:
        """
        A Rect describing the characteristics of the projection's far plane.
        """

    @abstractmethod
    def clip_to_NDC(self, clip_coords: Vector3) -> Vector3:
        """
        Takes a point in clip coordinates (the local space of the projection) and
        transforms it into NDC space.

        :param clip_coords: A 3D point in the clip coordinates of the projection.
            For 2D, the Z axis is ignored.
        :return: A 3D point in standard NDC space.
        """
        pass

    @abstractmethod
    def NDC_to_clip(self, ndc_coords: Vector3) -> Vector3:
        """
        Takes a point in NDC space and transforms it into clip coordinates

        :param ndc_coords: A 3D point in NDC space.
        :return: A 3D point in clip coordinates of the projection.
        """
        pass
