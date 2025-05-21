from __future__ import annotations

from typing import TYPE_CHECKING
from weakref import WeakKeyDictionary

from ..types import Renderer

if TYPE_CHECKING:
    from ..types import CameraBase
    from ..sprite import Sprite
    from pygame import Surface


class SpriteRenderer(Renderer):
    _sprite_cache: WeakKeyDictionary[Sprite, Surface] = WeakKeyDictionary()

    @classmethod
    def cull(cls, sprite: Sprite, camera: CameraBase) -> bool:
        if not (surface := cls._sprite_cache.get(sprite)):
            surface = sprite.draw_sprite()
            cls._sprite_cache[sprite] = surface
        rect = surface.get_rect()
        sprite.anchor.anchor_rect_ip(rect, sprite.transform.world_position)
        return camera._in_view(rect)

    @classmethod
    def render(cls, sprite: Sprite, camera: CameraBase):
        if sprite.is_dirty or sprite not in cls._sprite_cache:
            # Update the cache. This will save us redraws when the sprite is unchanged.
            sprite.is_dirty = False
            cls._sprite_cache[sprite] = sprite.draw_sprite()
        surface = cls._sprite_cache[sprite]
        position = sprite.anchor.anchor_rect(
            surface.get_rect(), sprite.transform.world_position
        )
        camera.draw_to_view(surface, position.topleft)
