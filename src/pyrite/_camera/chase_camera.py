from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from .camera import Camera
from ..entity import Entity

from pygame import Vector2

if TYPE_CHECKING:
    from .camera import Projection
    from ..enum import Layer
    from ..types import HasTransform, HasTransformProperty
    from pyrite._types.transform import TransformLike
    from .._rendering.viewport import Viewport
    from pygame.typing import Point


class ChaseCamera(Entity, Camera):

    def __init__(
        self,
        projection: Projection,
        position: Point = (0, 0),
        transform: TransformLike | None = None,
        render_targets: Viewport | Sequence[Viewport] | None = None,
        layer_mask: tuple[Layer] | None = None,
        target: HasTransform | HasTransformProperty | None = None,
        ease_factor: float = 8.0,
        max_distance: float = -1,
        relative_lag: bool = False,
        enabled=True,
    ) -> None:
        """
        A camera that is capable of chasing a target.

        :param projection: A camera projection describing the type of camera.
        :param position: Position of the origin of the projection, defaults to None
            None will give the center of the viewport.
        :param transform: A Transform or Transform Component for defining the location
            of the camera. If another object's TransformComponent is used, the camera
            will follow it. If a Transform is given, a new TransformComponent is given
            to the camera based on that value. If None, a new Transform is made from
            _position_.
        :param render_targets: Defines targets to render to. If multiple render targets
            are used, the camera will be rendered and scaled/cropped to each of them.
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
        :param enabled: Whether the Renderable will be drawn to the screen,
        defaults to True
        """
        Camera.__init__(
            self,
            projection,
            position,
            transform,
            render_targets,
            layer_mask,
            enabled,
        )
        Entity.__init__(
            self,
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
        assert Camera.enabled.fget
        return Camera.enabled.fget(self)

    @enabled.setter
    def enabled(self, value: bool) -> None:
        assert Camera.enabled.fset
        assert Entity.enabled.fset
        Camera.enabled.fset(self, value)
        Entity.enabled.fset(self, value)

    def post_update(self, delta_time: float) -> None:
        if not self.target:
            return
        delta = self.calculate_ease(
            self.transform.world_position - self.target.transform.world_position,
            delta_time,
        )
        if self.max_distance >= 0:
            delta = self.clamp_magnitude(delta)
        self.transform.world_position = self.target.transform.world_position + delta

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
        return self.clamp_magnitude(delta)

    def _clamp_magnitude_invariant(self, delta: Vector2) -> Vector2:
        return delta.clamp_magnitude(0, self.max_distance)

    def _clamp_magnitude_scaled(self, delta: Vector2) -> Vector2:
        return delta.clamp_magnitude(0, self.max_distance / self._zoom_level)
