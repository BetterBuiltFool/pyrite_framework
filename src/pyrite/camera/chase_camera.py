from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from .camera import Camera
from ..types.entity import Entity
from ..types.surface_sector import SurfaceSector

from pygame import Vector2

if TYPE_CHECKING:
    from ..types import HasPosition
    from pygame.typing import Point


class ChaseCamera(Camera, Entity):
    """
    A camera sub-type that can chase a target with a controllable easing factor and
    maximum distance.
    """

    def __init__(
        self,
        max_size: Point,
        position: Point = None,
        container=None,
        surface_sectors: SurfaceSector | Sequence[SurfaceSector] = None,
        smooth_scale: bool = False,
        enabled=True,
        draw_index=0,
        target: HasPosition = None,
        ease_factor: float = 8.0,
        max_distance: float = -1,
        relative_lag: bool = False,
    ) -> None:
        """
        A camera that is capable of chasing a target.

        :param max_size: Largest, most zoomed out size of the camera.
        :param position: Position of the center of the camera surface, defaults to None
        None will give the center of the viewport.
        :param surface_sectors: Defines sections of the screen to render to. If multiple
        surface sectors are used, the camera will be rendered and scaled to each of
        them.
        :param viewport: A rectangle representing the actual viewable area of the
        camera, defaults to None.
        None will give the center of the viewport.
        :param layer_mask: Layers that the camera will exclude from rendering,
        defaults to None
        :param container: The instance of the game to which the rengerable belongs,
        defaults to None. See Renderable.
        :param enabled: Whether the Renderable will be drawn to the screen,
        defaults to True
        :param draw_index: Index determining draw order within a layer, defaults to 0
        :param target: Object with a position to chase.
        :param ease_factor: Determines the rate at which the camera pursues the target.
        Larger = slower.
        :param max_distance: Maximum distance, in world space, that the target may be
        from the camera. Camera will "speed up" to maintain this distance.
        Negative numbers will disable.
        :param relative_lag: Bool determining if the max distance is relative to zoom
        level. If true, the max distance will be consistent within screen space.
        """
        if target and position is None:
            position = target.position
        Camera.__init__(
            self,
            max_size=max_size,
            position=position,
            surface_sectors=surface_sectors,
            smooth_scale=smooth_scale,
            container=container,
            enabled=enabled,
            draw_index=draw_index,
        )
        self.target = target
        self.ease_factor = ease_factor
        self.max_distance = max_distance
        """
        Maximum distance the camera may be from the target.
        Negative numbers will disable.
        """
        self.clamp_magnitude = (
            self._clamp_magnitude_invariant
            if not relative_lag
            else self._clamp_magnitude_scaled
        )

    def post_update(self, delta_time: float) -> None:
        if not self.target:
            return
        delta = self.calculate_ease(self.position - self.target.position, delta_time)
        if self.max_distance >= 0:
            delta = self.clamp_magnitude(delta)
        self.position: Vector2 = self.target.position + delta

    def calculate_ease(self, delta: Vector2, delta_time: float) -> Vector2:
        distance = delta.magnitude()
        if distance == 0:
            return delta
        delta_normalized = delta.normalize()
        distance_adjustment = distance / self.ease_factor
        distance_adjustment *= 60 * delta_time
        distance -= distance_adjustment

        return delta_normalized * distance

    def clamp_magnitude(self, delta: Vector2) -> Vector2:
        pass

    def _clamp_magnitude_invariant(self, delta: Vector2) -> Vector2:
        return delta.clamp_magnitude(0, self.max_distance)

    def _clamp_magnitude_scaled(self, delta: Vector2) -> Vector2:
        return delta.clamp_magnitude(0, self.max_distance / self._zoom_level)
