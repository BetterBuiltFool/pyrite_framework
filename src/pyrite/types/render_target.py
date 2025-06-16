from __future__ import annotations

from typing import Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    from pygame import Rect, Surface


class RenderTarget(Protocol):

    def get_target_surface(self) -> Surface:
        """
        Gets the surface to be drawn to.
        """

    def get_target_rect(self) -> Rect:
        """
        Gets the Rect that represents the surface space of the RenderTarget.
        """

    @property
    def crop(self) -> bool:
        """
        Determines if the rendering should be cropped or not.
        If False, the rendering will be scaled to fit the target.
        """
