from __future__ import annotations

from functools import singledispatchmethod


class Layer:

    def __init__(self, render_index: int = None) -> None:
        self._render_index = render_index

    @property
    def render_index(self) -> int:
        return self._render_index

    @render_index.setter
    def render_index(self, index: int):
        self._render_index = index


class RenderLayers:
    BACKGROUND = Layer(0)
    MIDGROUND = Layer(1)
    FOREGROUND = Layer(2)
    UI_LAYER = Layer(3)

    # Ordered set of layers
    _layers = [BACKGROUND, MIDGROUND, FOREGROUND, UI_LAYER]

    @classmethod
    def add_layer(cls, layer: Layer):
        if layer._render_index is None:
            # No index? Put it just behind UI layer
            layer._render_index = len(cls._layers) - 1
        cls._layers.insert(layer._render_index, layer)
        # Update indexes to preserve seperation.
        cls._reorder_layers()

    @classmethod
    def _reorder_layers(cls):
        for index, render_layer in enumerate(cls._layers):
            render_layer._render_index = index

    @classmethod
    def _get_layer_name(cls, layer: Layer) -> str:
        name = layer.__repr__
        match layer:
            case cls.BACKGROUND:
                name = "Background"
            case cls.MIDGROUND:
                name = "Midground"
            case cls.FOREGROUND:
                name = "Foreground"
            case cls.UI_LAYER:
                name = "UI Layer"
        return name

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
        ):
            raise ValueError(
                f"Attempted to remove layer '{cls._get_layer_name(item)}'; Cannot "
                "remove built-in layers"
            )
        layer = cls._layers.remove(item)
        cls._reorder_layers()
        return layer

    @remove_layer.register
    @classmethod
    def _(cls, layer: Layer) -> Layer:
        """
        Removes a layer from the layer list, and relabels the indices of the
        remaining layers.

        Will not remove built-in layers.

        :param layer: The layer to be removed.
        :return: The removed layer
        :raises ValueError: Raised if the layer is not a part of the layer list, or if
        the layer to be removed is one of the built-in layers.
        """

    @remove_layer.register
    @classmethod
    def _(cls, index: int) -> Layer:
        """
        Removes the layer at the given index from the layer list, and relabels the
        indices of the remaining layers.

        Will not remove built-in layers.

        :param index: The layer to be removed.
        :return: The removed layer
        :raises IndexError: Raised if the index is invalid.
        :raises ValueError: Raised if the index belongs to a built-in layer.
        """
