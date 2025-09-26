from __future__ import annotations

import typing

from pyrite.enum import AnchorPoint
from pyrite._rendering.rect_bounds import RectBounds, rotate_rect
from pyrite._rendering.base_renderable import BaseRenderable as Renderable
from pyrite._rendering.sprite_renderer import SpriteRendererProvider as SpriteRenderer
from pyrite._services.bounds_service import BoundsServiceProvider as BoundsService
from pyrite._component.transform_component import TransformComponent
from pyrite._types.sprite import Sprite


if typing.TYPE_CHECKING:
    from pygame import Surface, Vector2
    from pygame.typing import Point
    from pyrite._types.camera import Camera
    from pyrite._types.bounds import CullingBounds
    from pyrite._types.protocols import TransformLike
    from pyrite.enum import Layer, Anchor


class BaseSprite(Sprite, Renderable):
    """
    A basic renderable with a world position and a surface to display.
    """

    def __init__(
        self,
        display_surface: Surface,
        position: Point = (0, 0),
        local_transform: TransformLike | None = None,
        anchor: Anchor = AnchorPoint.CENTER,
        enabled=True,
        layer: Layer | None = None,
        draw_index=0,
    ) -> None:
        """
        A basic renderable that displays a surface at a world position.

        :param display_surface: The image or surface to be shown.
        :param position: Location of the Decor object, in world space,
        defaults to (0, 0)
        :param anchor: AnchorPoint that determines where on the object the position
        references, defaults to Anchor.CENTER
        :param enabled: Whether or not the object should be active immediately upon
        spawn, defaults to True
        :param layer: Render layer to which the object belongs, defaults to None
        :param draw_index: Draw order for the renderable, defaults to 0
        """
        super().__init__(enabled, layer, draw_index)
        self._reference_image = display_surface
        # self.display_surface = display_surface
        self.transform: TransformComponent
        if local_transform is not None:
            if isinstance(local_transform, TransformComponent):
                # If we're being passed something else's transform,
                # we'll just use that instead.
                self.transform = local_transform
            else:
                self.transform = TransformComponent.from_transform(
                    self, local_transform
                )
        else:
            self.transform = TransformComponent.from_attributes(self, position)

        self.anchor = anchor

        # Clients can update these easily enough.
        self._flip_x = False
        self._flip_y = False

        self._is_dirty = True

    @property
    def position(self) -> Vector2:
        return self.transform.position

    @position.setter
    def position(self, position: Point):
        self.transform.position = position

    @property
    def flip_x(self) -> bool:
        """
        Shows if the image is set to be flipped along the x axis.
        """
        return self._flip_x

    @flip_x.setter
    def flip_x(self, flip_x: bool):
        """
        Sets the sprite to be flipped along the x axis.
        Note: setting this directly will not automatically flip the display. Use
        set_surface() for that, or call _force_update_surface() after setting the flip
        parameters.

        :param flip_x: Boolean determining whether to flip the sprite image.
        """
        self._flip_x = flip_x

    @property
    def flip_y(self) -> bool:
        """
        Shows if the image is set to be flipped along the y axis.
        """
        return self._flip_y

    @flip_y.setter
    def flip_y(self, flip_y: bool):
        """
        Sets the sprite to be flipped along the y axis.
        Note: setting this directly will not automatically flip the display. Use
        set_surface() for that, or call _force_update_surface() after setting the flip
        parameters.

        :param flip_y: Boolean determining whether to flip the sprite image.
        """
        self._flip_y = flip_y

    @property
    def is_dirty(self) -> bool:
        return self._is_dirty

    @is_dirty.setter
    def is_dirty(self, is_dirty: bool):
        self._is_dirty = is_dirty

    def set_surface(
        self,
        sprite_image: Surface | None = None,
        flip_x: bool | None = None,
        flip_y: bool | None = None,
    ):
        """
        Changes the sprite's display to match the given properties.
        If any parameter is None, it uses the sprite's current setting.

        :param sprite_image: The raw surface being used, defaults to None
        :param flip_x: Whether to flip along the x axis, defaults to None
        :param flip_y: Whether to flip along the y axis, defaults to None
        """
        sprite_image = (
            sprite_image if sprite_image is not None else self._reference_image
        )
        flip_x = flip_x if flip_x is not None else self.flip_x
        flip_y = flip_y if flip_y is not None else self.flip_y

        self.flip_x, self.flip_y = flip_x, flip_y

        self._reference_image = sprite_image

        self.is_dirty = True

    def get_surface(self) -> Surface:
        return self._reference_image

    def get_bounds(self) -> CullingBounds:
        bounds, transform = BoundsService.get(self)
        if bounds is None or transform != self.transform.world():
            transform = self.transform.world()
            display_rect = self._reference_image.get_rect()
            scale = transform.scale

            center = self.anchor.get_rect_center(
                display_rect, transform.position, transform.rotation, scale
            )

            width, height = display_rect.size
            width *= scale.x
            height *= scale.y
            display_rect.size = width, height
            pivot = self.anchor.get_center_offset(display_rect)

            bounds_rect = rotate_rect(display_rect, transform.rotation, pivot)
            bounds_rect.center = center

            bounds = RectBounds(bounds_rect)
            transform = self.transform.world()
            BoundsService.set(self, (bounds, transform))

        return bounds

    def render(self, delta_time: float, camera: Camera):
        SpriteRenderer.render(delta_time, self, camera)
