from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING

from .camera import Camera
from ..types.entity import Entity
from .surface_sector import SurfaceSector

from pygame import Vector2
import pygame

if TYPE_CHECKING:
    from ..types import HasTransform
    from pygame.typing import Point

    # from ..transform import TransformComponent


class ChaseCamera(Entity):
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
        target: HasTransform = None,
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
            position = target.transform.position
        self.camera = Camera(
            max_size=max_size,
            position=position,
            surface_sectors=surface_sectors,
            smooth_scale=smooth_scale,
            container=container,
            enabled=enabled,
            draw_index=draw_index,
        )
        super().__init__(container, enabled)
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

    @property
    def position(self) -> Point:
        return self.camera.position

    @position.setter
    def position(self, position: Point):
        self.camera.position = Vector2(position)

    @property
    def smooth_scale(self) -> bool:
        return self.camera.smooth_scale

    @smooth_scale.setter
    def smooth_scale(self, flag: bool):
        self.camera.smooth_scale = flag

    def clear(self):
        """
        Overwrite the surface to allow new drawing on top.
        Basic camera fills with transparent black.
        """
        self.camera.clear()

    def get_surface_rect(self) -> pygame.Rect:
        """
        Gets the rect of the camera's surface, in worldspace, centered on the position.

        :return: A Rectangle matching the size of the camera surface, in worldspace.
        """
        return self.camera.get_surface_rect()

    def get_viewport_rect(self) -> pygame.Rect:
        """
        Gives the viewport converted to worldspace.

        :return: A Rectangle matching the size of the viewport, with worldspace
        coordinates.
        """
        return self.camera.get_viewport_rect()

    def to_local(self, point: Point) -> Vector2:
        return self.camera.to_local(point)

    def to_world(self, point: Point) -> Vector2:
        return self.camera.to_world(point)

    def screen_to_world(self, point: Point, sector_index: int = 0) -> Vector2:
        """
        Converts a screen coordinate into world coordinates.
        If the screen coordinate is outside the surface sector, it will extrapolate to
        find the equivalent space.

        :param point: A location in screen space, usually pygame.mouse.get_pos()
        :param sector_index: Index of the sector to compare against, defaults to 0.
        :raises IndexError: If the sector_index is larger than the camera's
        number of sectors.
        :return: The screen position, in world space relative to the camera
        """
        return self.camera.screen_to_world(point, sector_index)

    def screen_to_world_clamped(
        self, point: Point, sector_index: int = 0
    ) -> Vector2 | None:
        """
        Variant of screen_to_world.
        Converts a screen coordinate into world coordinates.
        If the screen coordinate is outside the surface sector, it will instead return
        None.

        Use this when it needs to be clear that the mouse is outside the camera
        view.

        :param point: A location in screen space, usually pygame.mouse.get_pos()
        :param sector_index: Index of the sector to compare against, defaults to 0.
        :raises IndexError: If the sector_index is larger than the camera's
        number of sectors.
        :return: The screen position, in world space relative to the camera
        """

        return self.camera.screen_to_world_clamped(point, sector_index)

    def post_update(self, delta_time: float) -> None:
        if not self.target:
            return
        delta = self.calculate_ease(
            self.position - self.target.transform.position, delta_time
        )
        if self.max_distance >= 0:
            delta = self.clamp_magnitude(delta)
        self.position: Vector2 = self.target.transform.position + delta

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
        return delta.clamp_magnitude(0, self.max_distance / self.camera._zoom_level)

    def zoom(self, zoom_level: float):
        self.camera.zoom(zoom_level)
