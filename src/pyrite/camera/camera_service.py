from __future__ import annotations

from typing import TYPE_CHECKING
from weakref import WeakKeyDictionary

import pygame
from pygame import Surface, Vector2

if TYPE_CHECKING:
    from . import Camera
    from pygame.typing import Point


class CameraService:

    _surfaces: WeakKeyDictionary[Camera, Surface] = WeakKeyDictionary()

    @classmethod
    def add_camera(
        cls, camera: Camera, camera_surface: Surface = None, max_size: Point = None
    ):
        if not camera_surface:
            if not max_size:
                max_size = pygame.display.get_surface().size
            max_size = Vector2(max_size)
            camera_surface = Surface(max_size)
        cls._surfaces.update({camera: camera_surface})

    @classmethod
    def draw_to_camera(cls, camera: Camera, image: Surface, position: Point):
        surface = cls._surfaces.get(camera)
        surface.blit(image, camera.to_local(position))
