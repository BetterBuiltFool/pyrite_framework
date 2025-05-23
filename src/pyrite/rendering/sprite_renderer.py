from __future__ import annotations

from typing import TypeAlias, TYPE_CHECKING
from weakref import WeakKeyDictionary

from ..types import Renderer

if TYPE_CHECKING:
    from ..types import CameraBase, Transform
    from ..sprite import Sprite
    from pygame import Surface

    SpriteData: TypeAlias = tuple[Surface, Transform]


class SpriteRenderer(Renderer):
    _sprite_cache: WeakKeyDictionary[Sprite, SpriteData] = WeakKeyDictionary()

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
    def render(cls, sprite: Sprite, camera: CameraBase):
        surface, transform = cls.get(sprite)
        if surface is None or not cls.validate_sprite(sprite, surface, transform):
            # Update the cache. This will save us redraws when the sprite is unchanged.
            surface = sprite.draw_sprite()
            cls._sprite_cache.update({sprite: (surface, sprite.transform.world())})
            sprite.is_dirty = False

        position = sprite.anchor.anchor_rect(
            surface.get_rect(), sprite.transform.world_position
        )
        camera.draw_to_view(surface, position.topleft)
