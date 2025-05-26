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
