from __future__ import annotations

from typing import TYPE_CHECKING
from weakref import WeakKeyDictionary

from pygame import Surface, Vector2

from ..rendering.view_plane import ViewPlane
from ..rendering.rect_bounds import RectBounds

if TYPE_CHECKING:
    from .camera import Camera
    from ..types import CameraViewBounds, CullingBounds
    from pygame import Rect
    from pygame.typing import Point


class CameraService:

    _surfaces: WeakKeyDictionary[Camera, Surface] = WeakKeyDictionary()

    @classmethod
    def add_camera(cls, camera: Camera):
        """
        Adds the camera to the service.

        :param camera: The Camera object being added.
        """
        cls._rebuild_surface(camera)

    @classmethod
    def clear(cls, camera: Camera):
        surface = cls._surfaces.get(camera)
        surface.fill((0, 0, 0))

    @classmethod
    def draw_to_camera(cls, camera: Camera, image: Surface, position: Point):
        surface = cls._surfaces.get(camera)
        surface.blit(image, camera.to_local(position))

    @classmethod
    def get_bounds(cls, camera: Camera) -> CullingBounds:
        return RectBounds(cls.get_rect(camera))

    @classmethod
    def get_rect(cls, camera: Camera) -> Rect:
        surface = cls._surfaces.get(camera)
        return surface.get_rect()

    @classmethod
    def get_view_bounds(cls, camera: Camera) -> CameraViewBounds:
        return ViewPlane(cls._get_view_rect(camera))

    @classmethod
    def _get_view_rect(cls, camera: Camera) -> Rect:
        surface = cls._surfaces.get(camera)
        surface_rect = surface.get_rect().copy()
        surface_rect.center = camera.transform.world_position
        return surface_rect

    @classmethod
    def _rebuild_surface(cls, camera: Camera):
        zoom_factor = 1 / camera.zoom_level
        display_size = camera.projection.far_plane.size
        surface_size = (display_size[0] * zoom_factor), (display_size[1] * zoom_factor)
        surface = Surface(surface_size)
        cls._surfaces.update({camera: surface})

    @classmethod
    def to_local(cls, camera: Camera, point: Point) -> Point:
        # TODO Slog through this and make it work
        # It renders correctly, but bounds end up mirrored above the sprites.
        # point = Vector2(point)

        # point -= Vector2(self.get_surface_rect().bottomleft)

        # point.y = -point.y

        # return point
        return point - Vector2(cls._get_view_rect(camera).topleft)

    @classmethod
    def to_world(cls, camera: Camera, point: Point) -> Point:
        # point = Vector2(point)

        # point += Vector2(self.get_surface_rect().bottomleft)

        # point.y = -point.y

        # return point

        surface = cls._surfaces.get(camera)
        surface_rect = surface.get_rect().copy()
        surface_rect.center = camera.transform.world_position
        return point + Vector2(surface_rect.topleft)

    @classmethod
    def screen_to_world(
        cls, camera: Camera, point: Point, viewport_index: int = 0
    ) -> Point:
        # viewport = self.viewports[viewport_index]
        # viewport_rect = self._get_viewport_rect(viewport)

        # viewport_world = self.get_viewport_rect()

        # viewport_space_position = self._screen_to_viewport(
        #     point, viewport_rect, Vector2(viewport_world.size)
        # )

        # return viewport_space_position.elementwise() + viewport_world.topleft
        pass

    @classmethod
    def screen_to_world_clamped(
        cls, camera: Camera, point: Point, viewport_index: int = 0
    ) -> Point | None:
        # viewport = self.viewports[viewport_index]
        # viewport_rect = self._get_viewport_rect(viewport)

        # if not viewport_rect.collidepoint(point):
        #     return None

        # viewport_world = self.get_viewport_rect()

        # viewport_space_position = self._screen_to_viewport(
        #     point, viewport_rect, Vector2(viewport_world.size)
        # )

        # return viewport_space_position.elementwise() + viewport_world.topleft
        pass

    @classmethod
    def zoom(cls, camera: Camera, zoom: float):
        cls._rebuild_surface(camera)

    @classmethod
    def zoom_to(cls, camera: Camera, size: Point):
        display_size = camera.projection.far_plane.size
        zoom_x = display_size[0] / size[0]
        zoom_y = display_size[1] / size[1]
        camera.zoom = (zoom_x, zoom_y)
