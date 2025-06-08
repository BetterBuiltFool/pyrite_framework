from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, TypeVar

from pyrite.types import Container

from .camera import Camera
from ..types.entity import Entity

from pygame import Vector2

if TYPE_CHECKING:
    from ..enum import Layer
    from ..types import (
        HasTransform,
        TransformProtocol,
    )
    from ..types.projection import Projection
    from ..rendering.viewport import Viewport
    from pygame.typing import Point

    P = TypeVar("P", bound=Projection)


class ChaseCamera(Entity, Camera):

    def __init__(
        self,
        projection: P,
        position: Point = (0, 0),
        transform: TransformProtocol = None,
        viewports: Viewport | Sequence[Viewport] = None,
        smooth_scale: bool = False,
        layer_mask: tuple[Layer] = None,
        target: HasTransform = None,
        ease_factor: float = 8.0,
        max_distance: float = -1,
        relative_lag: bool = False,
        container: Container = None,
        enabled=True,
    ) -> None:
        """
        A camera that is capable of chasing a target.

        :param projection: A camera projection describing the type of camaera.
        :param position: Position of the center of the camera surface, defaults to None
        None will give the center of the viewport.
        :param viewports: Defines sections of the screen to render to. If multiple
        surface viewports are used, the camera will be rendered and scaled to each of
        them.
        :param smooth_scale: Determines if the scaling operation should use the smooth
            variety, defaults to False
        :param layer_mask: Layers that the camera will exclude from rendering,
        defaults to None
        :param target: Object with a position to chase.
        :param ease_factor: Determines the rate at which the camera pursues the target.
        Larger = slower.
        :param max_distance: Maximum distance, in world space, that the target may be
        from the camera. Camera will "speed up" to maintain this distance.
        Negative numbers will disable.
        :param relative_lag: Bool determining if the max distance is relative to zoom
        level. If true, the max distance will be consistent within screen space.
        :param container: The instance of the game to which the rengerable belongs,
        defaults to None. See Renderable.
        :param enabled: Whether the Renderable will be drawn to the screen,
        defaults to True
        :param draw_index: Index determining draw order within a layer, defaults to 0
        """
        Entity.__init__(
            self,
            container,
            enabled,
        )
        Camera.__init__(
            self,
            projection,
            position,
            transform,
            viewports,
            smooth_scale,
            layer_mask,
            container,
            enabled,
        )
        self.target = target
        self.ease_factor = ease_factor
        self.max_distance = max_distance
        self.clamp_magnitude = (
            self._clamp_magnitude_invariant
            if not relative_lag
            else self._clamp_magnitude_scaled
        )

    @property
    def enabled(self) -> bool:
        return Camera.enabled.fget(self)

    @enabled.setter
    def enabled(self, value: bool) -> None:
        Camera.enabled.fset(self, value)
        Entity.enabled.fset(self, value)

    def post_update(self, delta_time: float) -> None:
        if not self.target:
            return
        delta = self.calculate_ease(
            self.transform.world_position - self.target.transform.position, delta_time
        )
        if self.max_distance >= 0:
            delta = self.clamp_magnitude(delta)
        self.transform.world_position = self.target.transform.position + delta

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
