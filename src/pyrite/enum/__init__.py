from __future__ import annotations

from functools import singledispatchmethod
from typing import TYPE_CHECKING

from pygame import Rect, Vector2

if TYPE_CHECKING:
    from pygame.typing import Point, RectLike


class Layer:

    def __init__(self, render_index: int = None, name: str = "") -> None:
        self._render_index = render_index
        self._name = name

    @property
    def render_index(self) -> int:
        return self._render_index

    @render_index.setter
    def render_index(self, index: int):
        self._render_index = index

    @property
    def name(self) -> str:
        if not self._name:
            return self._render_index
        return self._name


class RenderLayers:
    BACKGROUND = Layer(0, "Background")
    MIDGROUND = Layer(1, "Midground")
    FOREGROUND = Layer(2, "Foreground")
    UI_LAYER = Layer(3, "UI Layer")
    """
    Special layer that is drawn in camera space, not world space.
    """
    CAMERA = Layer(-1, "Camera")
    """
    Special layer for camera objects. Not in the layer sequence. Always draw last.
    """

    # Ordered set of layers
    _layers = (BACKGROUND, MIDGROUND, FOREGROUND)

    @classmethod
    def add_layer(cls, layer: Layer):
        """
        Inserts the new layer into the enum. The layer is assigned based on its
        render_index. If the render index is None, the layer is placed second to last,
        just before the UI layer (To ensure UI is always drawn last.)

        :param layer: Layer object being inserted.
        """
        # Convert to list for easy modification
        layers = list(cls._layers)
        if layer._render_index is None:
            # No index? Just put it on the end.
            layer._render_index = len(layers)
        layers.insert(layer._render_index, layer)
        # Convert back to tuple and update the class attribute
        # Tuples may be more efficient in some use cases.
        cls._layers = tuple(layers)
        # Update indexes to preserve seperation.
        cls._reorder_layers()

    @classmethod
    def _reorder_layers(cls):
        """
        Updates indexes of the layers to match their index in the sequence to ensure
        they are contiguous.

        Gaps in the render indices could cause issues for a renderer if it assumes
        contiguity.
        """
        for index, render_layer in enumerate(cls._layers):
            render_layer._render_index = index

    @singledispatchmethod
    @classmethod
    def remove_layer(cls, item: Layer | int) -> Layer:
        if isinstance(item, int):
            # Throws IndexError if invalid
            item = cls._layers[item]
        # item is now always a layer object. It will have failed otherwise.
        if any(
            item == cls.BACKGROUND,
            item == cls.MIDGROUND,
            item == cls.FOREGROUND,
            item == cls.UI_LAYER,
            item == cls.CAMERA,
        ):
            raise ValueError(
                f"Attempted to remove layer '{item.name}'; Cannot "
                "remove built-in layers"
            )
        layers = list(cls._layers)
        layer = layers.remove(item)
        cls._layers = tuple(layers)
        cls._reorder_layers()
        return layer

    @remove_layer.register
    @classmethod
    def _(cls, layer: Layer) -> Layer:
        """
        Removes a layer from the layer sequence, and relabels the indices of the
        remaining layers.

        Will not remove built-in layers.

        :param layer: The layer to be removed.
        :return: The removed layer
        :raises ValueError: Raised if the layer is not a part of the layer sequence, or
        if the layer to be removed is one of the built-in layers.
        """

    @remove_layer.register
    @classmethod
    def _(cls, index: int) -> Layer:
        """
        Removes the layer at the given index from the layer sequence, and relabels the
        indices of the remaining layers.

        Will not remove built-in layers.

        :param index: The layer to be removed.
        :return: The removed layer
        :raises IndexError: Raised if the index is invalid.
        :raises ValueError: Raised if the index belongs to a built-in layer.
        """


class Anchor:
    """
    Defines, relative to a rectangle, what spot is considered the position.
    """

    def __init__(self, relative_position: Point) -> None:
        """
        Creates an anchor point, defining a relative point for the location of
        the position of a rectangle.

        :param relative_position: (0, 0) is top left, and (1, 1) is bottom right.
        """
        self._relative_position = Vector2(relative_position)

    def get_rect_center(
        self,
        rectangle: RectLike,
        position: Point,
        angle: float = 0,
        scale: Point = (1, 1),
    ) -> Vector2:
        """
        Calculates the new center of a rect with a given position, angle, and scaling.

        :param rectangle: A Rect-like pattern capturing the bounds of a raw Rect. The
            location is unimportant.
        :param position: The nominal position of the rectangle object, given the Anchor
            point.
        :param angle: The nominal rotation of the rectangle around its pivot, defaults
            to 0
        :param scale: The scaling factor of the rectangle, defaults to (1, 1)
        :return: A point in space of the center of a rectangle with the rotation,
            scaling, and position specified
        """
        rect = Rect(rectangle)
        pivot = self.get_center_offset(rect)
        pivot_scaled: Vector2 = pivot.elementwise() * scale
        rot_pivot = pivot_scaled.rotate(-angle)
        return position + rot_pivot

    def anchor_rect(self, rectangle: RectLike, position: Point, angle: float) -> Rect:
        rect = Rect(rectangle)
        self.anchor_rect_ip(rect, position, angle)
        return rect

    def anchor_rect_ip(self, rectangle: Rect, position: Point, angle: float) -> None:
        pivot: Vector2 = self._relative_position.elementwise() * rectangle.size
        pivot = pivot.rotate(-angle)
        offset = Vector2(position) - pivot
        rectangle.topleft = offset

    def get_center_offset(self, rectangle: Rect) -> Vector2:
        """
        Calculates the center offset from the rectangle.

        :return: Vector2 representing the difference between the rectangle's center and
            the pivot point described by the anchor.
        """
        pivot: Vector2 = self._relative_position.elementwise() * rectangle.size
        pivot += rectangle.topleft
        return pivot - rectangle.center


class AnchorPoint:
    """
    An enum for modifying the position of a rectangle for renderables.
    """

    TOPLEFT = Anchor((0, 0))
    MIDTOP = Anchor((0.5, 0))
    TOPRIGHT = Anchor((1, 0))
    MIDLEFT = Anchor((0, 0.5))
    CENTER = Anchor((0.5, 0.5))
    MIDRIGHT = Anchor((1, 0.5))
    BOTTOMLEFT = Anchor((0, 1))
    MIDBOTTOM = Anchor((0.5, 1))
    BOTTOMRIGHT = Anchor((1, 1))
