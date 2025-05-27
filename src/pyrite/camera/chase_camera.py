from __future__ import annotations

from collections.abc import Sequence
from typing import TYPE_CHECKING, TypeVar

from .camera import Camera
from ..types.entity import Entity
from ..transform import transform_component

from pygame import Vector2
import pygame

if TYPE_CHECKING:
    from ..rendering.rect_bounds import RectBounds
    from ..types import (
        CameraViewBounds,
        CameraBase,
        HasTransform,
        TransformProtocol,
    )
    from ..types.projection import Projection
    from .surface_sector import SurfaceSector
    from pygame.typing import Point
    from pygame import Surface

    P = TypeVar("P", bound=Projection)

    # from ..transform import TransformComponent


class ChaseCamera(Entity):
    """
    A camera sub-type that can chase a target with a controllable easing factor and
    maximum distance.
    """

    def __init__(
        self,
        projection: P,
        position: Point = (0, 0),
        transform: TransformProtocol = None,
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
        if transform is not None:
            if isinstance(transform, transform_component.TransformComponent):
                # If we're being passed something else's transform,
                # we'll just use that instead.
                self.transform = transform
            else:
                self.transform = transform_component.from_transform(self, transform)
        else:
            self.transform = transform_component.from_attributes(self, position)
        # if target and position is None:
        #     position = target.transform.position
        self.camera = Camera(
            projection=projection,
            transform=transform,
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
    def smooth_scale(self) -> bool:
        return self.camera.smooth_scale

    @smooth_scale.setter
    def smooth_scale(self, flag: bool):
        self.camera.smooth_scale = flag

    def clear(self):
        self.camera.clear(self)

    def draw_to_view(self, surface: Surface, position: Point):
        self.camera.draw_to_view(self, surface, position)

    def get_bounds(self) -> RectBounds:
        return self.camera.get_bounds(self)

    def get_view_bounds(self) -> CameraViewBounds:
        return self.camera.get_view_bounds(self)

    def render(self, delta_time: float, camera: CameraBase):
        self.camera.render(delta_time, camera)

    def to_local(self, point: Point) -> Point:
        return self.camera.to_local(self, point)

    def to_world(self, point: Point) -> Vector2:
        return self.camera.to_world(self, point)

    def screen_to_world(self, point: Point, sector_index: int = 0) -> Point:
        return self.camera.screen_to_world(self, point, sector_index)

    def screen_to_world_clamped(
        self, point: Point, sector_index: int = 0
    ) -> Point | None:
        return self.camera.screen_to_world_clamped(self, point, sector_index)

    def scale_view(
        self, camera_surface: pygame.Surface, target_size: Point
    ) -> pygame.Surface:
        """
        Returns a scaled version of the camera's view surface using the camera's chosen
        scale method.

        :param camera_surface: the rendered camera surface
        :param target_size: Destination size of the surface
        :return: The scaled surface.
        """
        return self.camera._scale_method(camera_surface, target_size)

    def zoom(self, zoom_level: float):
        self.camera.zoom(zoom_level)

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
        return delta.clamp_magnitude(0, self.max_distance / self.camera._zoom_level)
