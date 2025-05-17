from __future__ import annotations

from typing import TYPE_CHECKING
from weakref import WeakKeyDictionary

if TYPE_CHECKING:
    from ..types import CameraBase
    from ..sprite import Sprite
    from pygame import Surface


class SpriteRenderer:
    _sprite_cache: WeakKeyDictionary[Sprite, Surface] = WeakKeyDictionary()

    @classmethod
    def render(cls, sprite: Sprite, camera: CameraBase):
        if sprite.is_dirty or sprite not in cls._sprite_cache:
            cls._sprite_cache[sprite] = sprite.draw_sprite()
        surface = cls._sprite_cache[sprite]
        camera.surface.blit(surface, camera.to_local(sprite.get_rect().topleft))
