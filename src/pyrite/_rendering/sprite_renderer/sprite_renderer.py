from __future__ import annotations

from abc import abstractmethod
from typing import cast, TYPE_CHECKING
from weakref import WeakKeyDictionary

import pygame
from pygame import Surface, Vector2

from pyrite._services.camera_service import CameraServiceProvider as CameraService
from pyrite._services.camera_service.camera_service import DefaultCameraService
from pyrite._types.camera import Camera
from pyrite._types.renderer import Renderer
from pyrite._types.sprite import Sprite

if TYPE_CHECKING:
    from pygame.typing import Point

    from pyrite._types.protocols import HasTransformAttributes
    from pyrite._transform.transform import Transform

    type SpriteData = tuple[Surface, Transform]


class SpriteRenderer(Renderer[Sprite, Camera]):

    @abstractmethod
    def validate_sprite(
        self,
        sprite: Sprite,
        surface: Surface | None,
        transform: HasTransformAttributes | None,
    ) -> bool:
        pass

    @abstractmethod
    def get_debug(self) -> bool:
        pass

    @abstractmethod
    def set_debug(self, flag: bool):
        pass


class DefaultSpriteRenderer(SpriteRenderer):

    def __init__(self) -> None:
        self._sprite_cache: WeakKeyDictionary[Sprite, SpriteData] = WeakKeyDictionary()
        self._debug = False

    def validate_sprite(
        self,
        sprite: Sprite,
        surface: Surface | None,
        transform: HasTransformAttributes | None,
    ) -> bool:
        current_transform = sprite.transform.world()
        if transform is None or surface is None:
            return False
        return all(
            [
                not sprite.is_dirty,
                transform.rotation == current_transform.rotation,
                transform.scale == current_transform.scale,
            ]
        )

    def set_debug(self, flag: bool):
        self._debug = flag
        if flag:
            self.redraw_sprite = self._redraw_sprite_debug
        else:
            self.redraw_sprite = self._redraw_sprite

    def get_debug(self) -> bool:
        return self._debug

    def get(self, key: Sprite) -> SpriteData | tuple[None, None]:
        return self._sprite_cache.get(key, (None, None))

    def render(self, renderable: Sprite, target: Camera):
        surface, transform = self.get(renderable)
        if surface is None or not self.validate_sprite(renderable, surface, transform):
            # Update the cache. This will save us redraws when the sprite is unchanged.
            # surface = sprite.draw_sprite()
            transform = renderable.transform.world()
            surface = self.redraw_sprite(renderable)
            self._sprite_cache[renderable] = (surface, transform)
            renderable.is_dirty = False

        assert transform

        position = renderable.anchor.get_rect_center(
            renderable.get_surface().get_rect(),
            renderable.transform.world_position,
            renderable.transform.world_rotation,
            renderable.transform.world_scale,
        )
        surface_rect = surface.get_rect()
        surface_rect.center = position

        draw_transform = transform.copy()
        draw_transform.position = surface_rect.bottomleft

        self._draw_to_camera(target, surface, draw_transform)

    def _get_surface_pos(self, camera: Camera, transform: Transform) -> Point:

        local_transform = camera.to_local(transform)
        eye_coords = camera.to_eye(local_transform)

        eye_position = eye_coords.position
        screen_pos = Vector2(
            eye_position.x,
            -eye_position.y,
        )
        return screen_pos - camera.projection.far_plane.topleft

    def _draw_to_camera(
        self, camera: Camera, sprite_surface: Surface, transform: Transform
    ):
        camera_service = cast(DefaultCameraService, CameraService._service)
        surface = camera_service._surfaces[camera]

        # local_position = camera.to_eye(camera.to_local(transform)).position
        # local_position = local_position - camera.projection.far_plane.topleft
        # local_position.y = surface.size[1] - local_position.y
        # ^ It's gotta be something to do with here.
        # what we need to do:
        # 1. Take a world pos
        # 2. Convert it to camera-local
        # 3. Find out where it belongs in the projection
        # 4. Convert that to the surface location
        # 5. Blit
        # I think I might be missing step 4.
        # Surface rect is (0, 0, farplane.size)
        # So we should just need to shift

        surface.blit(sprite_surface, self._get_surface_pos(camera, transform))

    def redraw_sprite(self, sprite: Sprite) -> Surface:
        return self._redraw_sprite(sprite)

    def _redraw_sprite(self, sprite: Sprite) -> Surface:
        new_surface = pygame.transform.flip(
            sprite.get_surface(), sprite.flip_x, sprite.flip_y
        )

        new_surface = pygame.transform.scale_by(
            new_surface, sprite.transform.world_scale
        )

        new_surface = pygame.transform.rotate(
            new_surface, sprite.transform.world_rotation
        )
        return new_surface

    def _redraw_sprite_debug(self, sprite: Sprite) -> Surface:
        new_surface = pygame.transform.flip(
            sprite.get_surface(), sprite.flip_x, sprite.flip_y
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
