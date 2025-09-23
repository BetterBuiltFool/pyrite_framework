from __future__ import annotations

from abc import ABC, abstractmethod
import bisect
from collections.abc import Iterable
from typing import cast, Self, TYPE_CHECKING
from weakref import WeakSet

from pygame import Surface

from pyrite.enum import RenderLayers

from pyrite._rendering.render_texture import RenderTextureComponent
from pyrite._services.camera_service import CameraServiceProvider as CameraService

if TYPE_CHECKING:
    from pyrite.enum import Layer
    from pyrite._types.camera import CameraBase as Camera
    from pyrite._types.renderable import Renderable
    from pyrite._types.debug_renderer import DebugRenderer

    type LayerDict = dict[Camera, list[Renderable]]
    type RenderQueue = dict[Layer, LayerDict]

EMPTY_LAYER_SET: set[Renderable] = set()

_active_render_manager: RenderManager


def get_render_manager() -> RenderManager:
    return _active_render_manager


def set_render_manager(manager: RenderManager):
    global _active_render_manager
    _active_render_manager = manager


_active_renderer: RenderSystem


def get_renderer() -> RenderSystem:
    return _active_renderer


def set_renderer(renderer: RenderSystem):
    global _active_renderer
    _active_renderer = renderer


_deferred_enables: set[Renderable] = set()


def enable(renderable: Renderable):
    """
    Enables the renderable with the active render manager.
    If no active render manager exists, the renderable is stored until one is created.

    :param renderable: A renderable to be enabled.
    """
    if _active_render_manager:

        return _active_render_manager.enable(renderable)
    _deferred_enables.add(renderable)


def disable(renderable: Renderable):
    """
    Disables the renderable in the active render manager.
    If not active render manager exists and the renderable is queued for enabling,
    it is removed from the queue.

    :param renderable: A renderable to be disabled.
    """
    if _active_render_manager:
        _active_render_manager.disable(renderable)
        return
    _deferred_enables.discard(renderable)


def is_enabled(renderable: Renderable) -> bool:
    """
    Determines if the passed renderable is currently considered enabled by the manager.

    :param item: Any renderable
    :return: True if currently enabled, False if disabled
    """
    if not _active_render_manager:
        return False
    return _active_render_manager.is_enabled(renderable)


class RenderManager(ABC):
    """
    An object for managing renderables. Can enable and disable them, and generates a
    render queue for the renderer.
    """

    def __new__(cls, *args, **kwds) -> Self:
        new_manager = super().__new__(cls)
        set_render_manager(new_manager)
        return new_manager

    def __init__(self) -> None:
        for renderable in _deferred_enables:
            self.enable(renderable)

    @abstractmethod
    def generate_render_queue(self) -> RenderQueue:
        """
        Generates a dict of renderables, in draw order.

        The keys are metadata used by the renderer to determine factors like layer
        culling and, partially, draw order. They can be of any type, but must be a type
        the render method knows how to handle.
        """
        pass

    @abstractmethod
    def enable(self, item: Renderable) -> bool:
        """
        Adds a Renderable to the collection of renderables.

        Does nothing if the item is not a renderable.

        :param item: Object being enabled. Objects that are not renderable will be
        skipped.
        :return: True if enable is successful, False if not, such as object already
        enabled.
        """
        pass

    @abstractmethod
    def disable(self, item: Renderable) -> bool:
        """
        Removes the item from the collection of renderables.

        :param item: Renderable being removed.
        :return: True if disable is successful, False if not, such as object already
        disabled.
        """
        pass

    @abstractmethod
    def is_enabled(self, item: Renderable) -> bool:
        """
        Determines if the passed renderable is currently considered enabled by the
        manager.

        :param item: Any renderable
        :return: True if currently enabled, False if disabled
        """
        pass

    @abstractmethod
    def get_number_renderables(self) -> int:
        """
        Returns the total number of renderables being tracked by the renderer.
        """
        pass

    @staticmethod
    def get_render_manager(**kwds) -> RenderManager:
        """
        Extracts a render manager from keyword arguments.
        Used for creating a render manager for a new Game instance
        """
        if (render_manager := kwds.get("render_manager", None)) is None:
            manager_type = get_default_render_manager_type()
            render_manager = manager_type()
        return render_manager


class RenderSystem(ABC):
    """
    Class responsible for drawing renderables to the screen.
    """

    def __new__(cls) -> Self:
        new_renderer = super().__new__(cls)
        set_renderer(new_renderer)
        return new_renderer

    @abstractmethod
    def render(
        self,
        window: Surface,
        delta_time: float,
        render_queue: RenderQueue,
    ):
        """
        Draws the items from the render queue onto the passed surface.

        :param window: The game window, receiving final draws
        :param render_queue: A list of items that need to be rendered to the surface.
        """
        pass

    @abstractmethod
    def get_rendered_last_frame(self) -> int:
        """
        Returns the number of rednerables that were actually drawn in the previous
        frame.
        """

    @staticmethod
    def get_renderer(**kwds) -> RenderSystem:
        """
        Extracts a renderer from keyword arguments.
        Used for creating a renderer for a new Game instance
        """
        if (renderer := kwds.get("renderer", None)) is None:
            renderer_type = get_default_renderer_type()
            renderer = renderer_type()
        return renderer

    @abstractmethod
    def add_debug_renderer(self, debug_renderer: DebugRenderer):
        """
        Adds a debug renderer that has methods to do draws at various points.
        """
        pass


def _get_draw_index(renderable: Renderable) -> int:
    """
    Sort key for sorting by draw index.
    """
    return renderable.draw_index


class DefaultRenderManager(RenderManager):

    def __init__(self) -> None:
        self.renderables: dict[Layer, WeakSet[Renderable]] = {}
        self._rendered_last_frame: int = 0

        super().__init__()

    # Does not need a buffer for renderables, they should *NOT* be generated during the
    # render phase.

    def enable(self, item: Renderable) -> bool:
        layer = item.layer
        if layer is None:
            # No layer set, force it to midground
            layer = RenderLayers.MIDGROUND
            item._layer = layer
        render_layer = self.renderables.setdefault(layer, WeakSet())

        # Check if this is a fresh enable
        newly_added = item not in render_layer

        render_layer.add(item)

        return newly_added

    def disable(self, item: Renderable):
        layer = item.layer

        render_layer = self.renderables.get(layer, WeakSet())

        # Check if this is a fresh disable
        newly_disabled = item in render_layer

        if newly_disabled:
            # Changing this to check newly_disabled to avoid redundant check from
            # discard
            render_layer.remove(item)

        return newly_disabled

    def is_enabled(self, item: Renderable) -> bool:
        return any((item in render_layer) for render_layer in self.renderables.values())

    def generate_render_queue(
        self,
    ) -> RenderQueue:
        render_queue: RenderQueue = {}
        cameras = CameraService.get_active_cameras()

        for layer in RenderLayers._layers:
            layer_set = cast(set, self.renderables.get(layer, EMPTY_LAYER_SET))
            layer_dict = self.precull(layer_set, layer, cameras)
            render_queue[layer] = layer_dict

        return render_queue

    def precull(
        self,
        layer_set: set[Renderable],
        layer: Layer,
        cameras: Iterable[Camera] | None = None,
    ) -> LayerDict:
        if not cameras:
            # Just give the full layer set if there's no camera, pygame will handle
            # culling for us.
            return {CameraService._default_camera: self.sort_layer(layer_set)}
        culled_dict: LayerDict = {}
        for camera in cameras:
            if layer in camera.layer_mask:
                continue
            visible = filter(camera.cull, layer_set)
            culled_dict[camera] = self.sort_layer(visible)
        return culled_dict

    def get_number_renderables(self) -> int:
        count = 0
        for layer_set in self.renderables.values():
            count += len(layer_set)
        return count

    def sort_layer(self, renderables: Iterable[Renderable]) -> list[Renderable]:
        """
        Sorts a sequence of renderables by draw_index, such that they are ordered
        0 -> Infinity | -Infinity -> -1

        :param renderables: list of renderables to sort
        :return: Sorted list
        """
        renderables = sorted(renderables, key=_get_draw_index)
        pivot = bisect.bisect_left(renderables, 0, key=_get_draw_index)
        negatives = renderables[:pivot]
        del renderables[:pivot]

        negatives.reverse()

        return renderables + negatives


class DefaultRenderSystem(RenderSystem):

    def __init__(self) -> None:
        self._debug_renderers: set[DebugRenderer] = set()

    def add_debug_renderer(self, debug_renderer: DebugRenderer):
        self._debug_renderers.add(debug_renderer)

    def render_layer(
        self,
        delta_time: float,
        layer_queue: Iterable[Renderable],
        camera: Camera,
    ):
        """
        Extracts the renderables from the layer_queue, and has them drawn to the
        camera.

        :param delta_time: Time passed since last frame.
        :param layer_queue: The ordered sequence of renderables to be drawn.
        :param camera: The camera being drawn to.
        """
        count = 0
        for renderable in layer_queue:
            count += 1
            renderable.render(delta_time, camera)
        self._rendered_last_frame += count

    def render_camera(
        self,
        delta_time: float,
        camera: Camera,
    ):
        """
        Draws the given camera to the window, at each of its surface viewports.

        :param delta_time: Time passed since last frame, if needed for any calculations.
        :param camera: Camera being drawn to the screen
        :param window: Game window being drawn to
        """
        for render_target in camera.render_targets:
            camera.render(delta_time, render_target)

    def render_ui(
        self,
        delta_time: float,
        ui_elements: Iterable[Renderable],
        window: Surface,
    ):
        """
        Goes through the ui elements, and draws them to the screen. They are already in
        screen space, so they do not get adjusted.

        :param delta_time: Time passed since last frame.
        :param ui_elements: The sequence of ui elements to be drawn, in order.
        :param cameras: The cameras being drawn to.
        """
        # for ui_element in ui_elements:
        #     ui_element.render(delta_time, window)

    def render(
        self,
        window: Surface,
        delta_time: float,
        render_queue: RenderQueue,
    ):
        self._rendered_last_frame = 0
        cameras = CameraService.get_render_cameras()

        for camera in cameras:
            camera.refresh()

        for render_texture_component in RenderTextureComponent.get_instances().values():
            render_texture_component.update_texture()

        for layer in RenderLayers._layers:
            layer_dict = render_queue.get(layer, {})
            for camera, render_sequence in layer_dict.items():
                if layer in camera.layer_mask:
                    continue
                self.render_layer(delta_time, render_sequence, camera)

        # Render any cameras to the screen.
        for camera in CameraService.get_active_cameras():
            self.render_camera(delta_time, camera)

        self._debug_draw_to_screen(cameras, render_queue)

        # Render the UI last.

    def _debug_draw_to_screen(
        self, cameras: Iterable[Camera], render_queue: RenderQueue
    ):
        for renderer in self._debug_renderers:
            renderer.draw_to_screen(cameras, render_queue)

    def get_rendered_last_frame(self) -> int:
        return self._rendered_last_frame


_default_render_manager_type = DefaultRenderManager


def get_default_render_manager_type() -> type[RenderManager]:
    return _default_render_manager_type


def set_default_render_manager_type(render_manager_type: type[RenderManager]):
    global _default_render_manager_type
    _default_render_manager_type = render_manager_type


_default_renderer_type = DefaultRenderSystem


def get_default_renderer_type() -> type[RenderSystem]:
    return _default_renderer_type


def set_default_renderer_type(renderer_type: type[RenderSystem]):
    global _default_renderer_type
    _default_renderer_type = renderer_type
