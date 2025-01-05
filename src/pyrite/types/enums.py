from __future__ import annotations

from functools import singledispatchmethod


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
    CAMERA = Layer(-1, "Camera")
    """Special layer for camera objects. Not in the layer sequence. Always draw last.
    """

    # Ordered set of layers
    _layers = (BACKGROUND, MIDGROUND, FOREGROUND, UI_LAYER)

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
            # No index? Put it just behind UI layer
            layer._render_index = len(layers) - 1
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
