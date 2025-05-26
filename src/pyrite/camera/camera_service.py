from __future__ import annotations

from typing import TYPE_CHECKING
from weakref import WeakKeyDictionary

import pygame
from pygame import Surface

if TYPE_CHECKING:
    from . import Camera
    from pygame.typing import Point


class CameraService:

    _surfaces: WeakKeyDictionary[Camera, Surface] = WeakKeyDictionary()

    @classmethod
    def add_camera(cls, camera: Camera):
        """
        Adds the camera to the service.

        :param camera: The Camera object being added.
        """
        camera_surface = Surface(pygame.display.get_surface().size)
        cls._surfaces.update({camera: camera_surface})

    @classmethod
    def draw_to_camera(cls, camera: Camera, image: Surface, position: Point):
        surface = cls._surfaces.get(camera)
        surface.blit(image, camera.to_local(position))

    @classmethod
    def zoom(cls, camera: Camera, zoom: Point):
        display_size = pygame.display.get_surface().size
        surface_size = (display_size[0] * zoom[0]), (display_size[1] * zoom[1])
        surface = Surface(surface_size)
        cls._surfaces.update({camera: surface})

    @classmethod
    def zoom_to(cls, camera: Camera, size: Point):
        display_size = pygame.display.get_surface().size
        zoom_x = display_size[0] / size[0]
        zoom_y = display_size[1] / size[1]
        camera.zoom = (zoom_x, zoom_y)
