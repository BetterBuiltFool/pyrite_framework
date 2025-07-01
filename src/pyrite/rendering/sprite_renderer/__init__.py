from __future__ import annotations

from typing import TYPE_CHECKING


from .sprite_renderer import SpriteRenderer, DefaultSpriteRenderer
from ...types import Camera, RendererProvider


if TYPE_CHECKING:
    from pygame import Surface

    from ...types import TransformLike
    from ... import Sprite


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
