from __future__ import annotations

from typing import TYPE_CHECKING


from pyrite._rendering.sprite_renderer.sprite_renderer import (
    SpriteRenderer,
    DefaultSpriteRenderer,
)
from pyrite._types.camera import CameraBase as Camera
from pyrite._types.renderer import RendererProvider


if TYPE_CHECKING:
    from pygame import Surface

    from pyrite._types.transform import TransformLike
    from pyrite._sprite.sprite import Sprite


class SpriteRendererProvider(RendererProvider[SpriteRenderer]):

    _renderer: SpriteRenderer = DefaultSpriteRenderer()

    @classmethod
    def render(cls, delta_time: float, sprite: Sprite, camera: Camera):
        cls._renderer.render(delta_time, sprite, camera)

    @classmethod
    def validate_sprite(
        cls, sprite: Sprite, surface: Surface | None, transform: TransformLike | None
    ) -> bool:
        return cls._renderer.validate_sprite(sprite, surface, transform)

    @classmethod
    def get_debug(cls) -> bool:
        return cls._renderer.get_debug()

    @classmethod
    def set_debug(cls, flag: bool):
        cls._renderer.set_debug(flag)
