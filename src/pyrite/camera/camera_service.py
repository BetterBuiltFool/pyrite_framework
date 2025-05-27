from __future__ import annotations

from typing import TYPE_CHECKING
from weakref import WeakKeyDictionary

from pygame import Surface

if TYPE_CHECKING:
    from . import Camera
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
        camera_surface = Surface(camera.max_size)
        cls._surfaces.update({camera: camera_surface})

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
        pass

    @classmethod
    def get_rect(cls, camera: Camera) -> Rect:
        surface = cls._surfaces.get(camera)
        return surface.get_rect()

    @classmethod
    def get_view_bounds(cls, camera: Camera) -> CameraViewBounds:
        pass

    @classmethod
    def to_local(cls, camera: Camera, point: Point) -> Point:
        # TODO Slog through this and make it work
        # It renders correctly, but bounds end up mirrored above the sprites.
        # point = Vector2(point)

        # point -= Vector2(self.get_surface_rect().bottomleft)

        # point.y = -point.y

        # return point

        # return point - Vector2(self.get_surface_rect().topleft)
        pass

    @classmethod
    def to_world(cls, camera: Camera, point: Point) -> Point:
        # point = Vector2(point)

        # point += Vector2(self.get_surface_rect().bottomleft)

        # point.y = -point.y

        # return point

        # return point + Vector2(self.get_surface_rect().topleft)
        pass

    @classmethod
    def screen_to_world(
        cls, camera: Camera, point: Point, sector_index: int = 0
    ) -> Point:
        # sector = self.surface_sectors[sector_index]
        # sector_rect = self._get_sector_rect(sector)

        # viewport_world = self.get_viewport_rect()

        # viewport_space_position = self._screen_to_viewport(
        #     point, sector_rect, Vector2(viewport_world.size)
        # )

        # return viewport_space_position.elementwise() + viewport_world.topleft
        pass

    @classmethod
    def screen_to_world_clamped(
        cls, camera: Camera, point: Point, sector_index: int = 0
    ) -> Point | None:
        # sector = self.surface_sectors[sector_index]
        # sector_rect = self._get_sector_rect(sector)

        # if not sector_rect.collidepoint(point):
        #     return None

        # viewport_world = self.get_viewport_rect()

        # viewport_space_position = self._screen_to_viewport(
        #     point, sector_rect, Vector2(viewport_world.size)
        # )

        # return viewport_space_position.elementwise() + viewport_world.topleft
        pass

    @classmethod
    def zoom(cls, camera: Camera, zoom: float):
        display_size = camera.max_size
        surface_size = (display_size[0] * zoom), (display_size[1] * zoom)
        surface = Surface(surface_size)
        cls._surfaces.update({camera: surface})

    @classmethod
    def zoom_to(cls, camera: Camera, size: Point):
        display_size = camera.max_size
        zoom_x = display_size[0] / size[0]
        zoom_y = display_size[1] / size[1]
        camera.zoom = (zoom_x, zoom_y)
