from __future__ import annotations

from typing import TypeAlias, TYPE_CHECKING
from weakref import WeakKeyDictionary

import pygame

from ..types import Renderer
from ..services import CameraService
from ..transform import Transform

if TYPE_CHECKING:
    from ..camera import Camera
    from ..sprite import Sprite
    from pygame import Surface

    SpriteData: TypeAlias = tuple[Surface, Transform]


class SpriteRenderer(Renderer):
    """
    Renderer class for rendering sprites to cameras.
    """

    _sprite_cache: WeakKeyDictionary[Sprite, SpriteData] = WeakKeyDictionary()
    _debug = False

    @classmethod
    def set_debug(cls, flag: bool):
        cls._debug = flag
        if flag:
            cls.redraw_sprite = cls._redraw_sprite_debug
        else:
            cls.redraw_sprite = cls._redraw_sprite

    @classmethod
    def get_debug(cls) -> bool:
        return cls._debug

    @classmethod
    def get(cls, key: Sprite) -> SpriteData | tuple[None, None]:
        return cls._sprite_cache.get(key, (None, None))

    @classmethod
    def validate_sprite(
        cls, sprite: Sprite, surface: Surface, transform: Transform
    ) -> bool:
        current_transform = sprite.transform.world()
        return all(
            [
                not sprite.is_dirty,
                transform.rotation == current_transform.rotation,
                transform.scale == current_transform.scale,
            ]
        )

    @classmethod
    def render(cls, delta_time: float, sprite: Sprite, camera: Camera):
        surface, transform = cls.get(sprite)
        if surface is None or not cls.validate_sprite(sprite, surface, transform):
            # Update the cache. This will save us redraws when the sprite is unchanged.
            # surface = sprite.draw_sprite()
            surface = cls.redraw_sprite(sprite)
            cls._sprite_cache.update({sprite: (surface, sprite.transform.world())})
            sprite.is_dirty = False

        position = sprite.anchor.get_rect_center(
            sprite._reference_image.get_rect(),
            sprite.transform.world_position,
            sprite.transform.world_rotation,
            sprite.transform.world_scale,
        )
        surface_rect = surface.get_rect()
        surface_rect.center = position

        # cls._draw_to_camera(camera, surface, surface_rect.bottomleft)
        cls._draw_to_camera(
            camera, surface, Transform(position=surface_rect.bottomleft)
        )

    @classmethod
    def _draw_to_camera(
        cls, camera: Camera, sprite_surface: Surface, transform: Transform
    ):
        surface = CameraService._service._surfaces.get(camera)
        local_position = camera.to_eye(camera.to_local(transform)).position
        local_position[1] = surface.size[1] - local_position[1]
        surface.blit(sprite_surface, local_position)

    @classmethod
    def redraw_sprite(cls, sprite: Sprite) -> Surface:
        return cls._redraw_sprite(sprite)

    @classmethod
    def _redraw_sprite(cls, sprite: Sprite) -> Surface:
        new_surface = pygame.transform.flip(
            sprite._reference_image, sprite.flip_x, sprite.flip_y
        )

        new_surface = pygame.transform.scale_by(
            new_surface, sprite.transform.world_scale
        )

        new_surface = pygame.transform.rotate(
            new_surface, sprite.transform.world_rotation
        )
        return new_surface

    @classmethod
    def _redraw_sprite_debug(cls, sprite: Sprite) -> Surface:
        new_surface = pygame.transform.flip(
            sprite._reference_image, sprite.flip_x, sprite.flip_y
        )
        # Draw a white border on our image for debug purposes
        pygame.draw.rect(new_surface, (255, 255, 255), new_surface.get_rect(), 1)

        new_surface = pygame.transform.scale_by(
            new_surface, sprite.transform.world_scale
        )

        new_surface = pygame.transform.rotate(
            new_surface, sprite.transform.world_rotation
        )
        return new_surface
