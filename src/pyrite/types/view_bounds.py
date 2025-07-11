from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..types.bounds import CullingBounds


class CameraViewBounds(ABC):
    """
    An object representing the viewing area of a camera.
    """

    @abstractmethod
    def contains(self, bounds: CullingBounds) -> bool:
        """
        Determines if the bounds are contained within the CameraViewBounds.

        :param bounds: A CullingBounds object that may or may not be within the
            CameraViewBounds
        :return: True if the view bounds contains the bounds, otherwise False
        """
        pass
