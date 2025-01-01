from __future__ import annotations

import asyncio
from collections.abc import Callable
import logging
from types import MethodType, TracebackType
from typing import Self, TYPE_CHECKING

from src.pyrite._data_classes.display_settings import DisplaySettings
from src.pyrite._data_classes.entity_manager import EntityManager
from src.pyrite._data_classes.metadata import Metadata
from src.pyrite._data_classes.timing_settings import TimingSettings

if TYPE_CHECKING:
    from src.pyrite.types.entity import Entity
    from src.pyrite.types.renderable import Renderable


import pygame

logger = logging.getLogger(__name__)

_active_instance: Game = None


def get_game_instance() -> Game:
    return _active_instance


class Game:
    """
    Base Game object to serve as a parent for your game.
    Holds onto data required for generating the window and performing the main loop.
    Only one game instance may be running at a time. Attempting to start a new instance
    will stop the previous instance.
    """

    def __new__(cls, *args, **kwds) -> Self:
        global _active_instance
        if _active_instance is not None:
            _active_instance.is_running = False
            logger.info(
                f"Stopping {_active_instance}, only one game may be running at a time."
            )
        logger.info("Starting new game instance.")
        _active_instance = super().__new__(cls)
        return _active_instance

    def __init__(self, **kwds) -> None:

        suppress_init: bool = kwds.get("suppress_init", False)
        self.debug_mode: bool = kwds.get("debug_mode", False)
        self.suppress_context_errors: bool = kwds.get("suppress_context_errors", False)
        """
        Whether errors generated during context manager function should be suppressed.
        """

        if not suppress_init:
            pygame.init()

        self.is_running = True
        self.clock = pygame.time.Clock()

        # Extract various settings and metadata from keyword arguments.
        # Creates defaults if none are provided.
        self.display_settings = DisplaySettings.get_display_settings(**kwds)
        self.metadata = Metadata.get_metadata(**kwds)
        self.timing_settings = TimingSettings.get_timing_settings(**kwds)

        # Get a surface the size of the requested resolution.
        # This way, a surface exists even if the a window hasn't been created.
        self.windows: pygame.Surface = pygame.Surface(self.display_settings.resolution)

        # Entity manager will handle holding onto all enabled entities, renderables,
        # and ui elements.
        # Note these are held in weaksets, and thus allow GC. Entities, etc., need
        # additional references to stay alive.
        self.entity_manager = EntityManager()

    def __enter__(self) -> Self:
        """
        Basicmost __enter__ implementation.
        """
        return self

    def __exit__(
        self,
        exception_type: type[Exception] | None,
        exception_value: Exception | None,
        traceback: TracebackType | None,
    ):
        """
        Context manager exit. Starts the game when closing, unless an error occurs.
        """
        if exception_value is None or self.suppress_context_errors:
            # suppress_context_errors allows us to start regardless of any errors,
            # and hides them from the output.
            self.main()
        return self.suppress_context_errors

    def enable(self, item: Entity | Renderable) -> None:
        self.entity_manager.enable(item)

    def disable(self, item: Entity | Renderable) -> None:
        self.entity_manager.disable(item)

    def create_window(self):
        """
        Generates a window from current display settings.
        Updates the icon, if possible.
        The game's window and display settings are updated to reflect the new window.
        """
        if self.metadata.icon is not None:
            pygame.display.set_icon(self.metadata.icon)
        self.window, self.display_settings = DisplaySettings.create_window(
            self.display_settings
        )

    def main(self):
        """
        The main entry point for the game. By default, calls start_game(), but can be
        overridden to have more complex starting logic.

        For example, a function could be called to create a special early loop for
        loading in resources before calling the main game loop.
        """
        self.create_window()
        self.start_game()

    def start_game(self) -> None:
        """
        Begins the main game loop, calling the update methods and the render methods.
        """

        accumulated_time: float = 0.0

        while self.is_running:
            accumulated_time = self._main_loop_body(accumulated_time)

    def _main_loop_body(self, accumulated_time: float) -> float:
        """
        Body of the main loop. Handles the accumulated time used by const_update.

        :param accumulated_time: Time taken since last const_update call
        :return: Residual accumulated_time
        """

        delta_time, accumulated_time = self._get_frame_time(
            self.timing_settings.fps_cap, accumulated_time
        )

        self.process_events(pygame.event.get())

        if self.timing_settings.tick_rate > 0:
            accumulated_time = self._fixed_update_block(
                self.timing_settings.fixed_timestep, accumulated_time
            )

        self._update_block(delta_time)

        pygame.display.set_caption(self.metadata.caption)
        self._render_block(self.window, delta_time)

        return accumulated_time

    def _get_frame_time(
        self, fps_cap: int, accumulated_time: float = 0
    ) -> tuple[float, float]:
        """
        Runs the clock delay, returning the passed time and adding it to the
        accumulated time.

        :param fps_cap: Maximum frame rate, 0 is uncapped.
        :param accumulated_time: Time since last const_update, passed from the main loop
        :return: Tuple containing delta_time and the modified accumulated time.
        """
        delta_time = self.clock.tick(fps_cap) / 1000
        accumulated_time += delta_time
        return (delta_time, accumulated_time)

    def _monkeypatch_method(self, method: Callable, new_method: Callable) -> None:
        """
        Internal method. Used to replace 'method' with 'new_method'.
        Update methods and render methods each have their own patching method.

        :param method: Method being replaced
        :param new_method: Replacement method
        """
        self.__dict__[method.__name__] = MethodType(new_method, self)

    def pre_update(self, delta_time: float) -> None:
        """
        Early update function. Used for game logic that needs to run _before_ the main
        update phase.

        :param delta_time: Actual time passed since last frame, in seconds.
        """
        for entity in self.entity_manager.entities:
            entity.pre_update(delta_time)

    def update(self, delta_time: float) -> None:
        """
        Main update function. Used for coordinating most of the game state changes
        required.

        :param delta_time: Actual time passed since last frame, in seconds.
        """
        for entity in self.entity_manager.entities:
            entity.update(delta_time)

    def post_update(self, delta_time: float) -> None:
        """
        Late update function. Used for game logic that needs to run _after_ the main
        update phase.

        :param delta_time: Actual time passed since last frame, in seconds.
        """
        for entity in self.entity_manager.entities:
            entity.post_update(delta_time)

    def const_update(self, delta_time: float) -> None:
        """
        Update function that runs at a constant rate. Useful for anything that is
        sensitive to variations in frame time, such as physics.

        This is a basic, naïve implementation of a fixed timestep, and can be a bit
        jittery, especially when the tick rate and frame rate are not multiples of
        eachother.

        For more info, see Glenn Fiedler's "Fix Your Timestep!"

        :param delta_time: Simulated time passed since last update. Passed in from the
        game's timing_settings.
        """
        for entity in self.entity_manager.entities:
            entity.const_update(delta_time)

    def patch_pre_update(self, new_pre_update: Callable) -> None:
        """
        Override the default pre_update method with the supplied function.
        Supplied function must match default pre_update signature.
        Signature is: (self: Game, delta_time: float)

        :param new_pre_update: Callable matching pre_update signature.
        """
        self._monkeypatch_method(self.pre_update, new_pre_update)

    def patch_update(self, new_update: Callable) -> None:
        """
        Override the default update method with the supplied function.
        Supplied function must match default update signature.
        Signature is: (self: Game, delta_time: float)

        :param new_update: Callable matching update signature.
        """
        self._monkeypatch_method(self.update, new_update)

    def patch_post_update(self, new_post_update: Callable) -> None:
        """
        Override the default post_update method with the supplied function.
        Supplied function must match default post_update signature.
        Signature is: (self: Game, delta_time: float)

        :param new_post_update: Callable matching post_update signature.
        """
        self._monkeypatch_method(self.post_update, new_post_update)

    def patch_const_update(self, new_const_update: Callable) -> None:
        """
        Override the default const_update method with the supplied function.
        Supplied function must match default const_update signature.
        Signature is: (self: Game, delta_time: float)

        :param new_const_update: Callable matching const_update signature.
        """
        self._monkeypatch_method(self.const_update, new_const_update)

    def _update_block(self, delta_time: float) -> None:
        """
        Calls all of the update phases, in order.

        :param delta_time: Actual time passed since last frame, in seconds.
        """
        self.pre_update(delta_time)
        self.update(delta_time)
        self.post_update(delta_time)

    def _fixed_update_block(self, timestep: float, accumulated_time: float) -> float:
        """
        Runs const_update so long as accumulated time is greater than the timestep.

        CAUTION: If const_update takes longer to run than the timestep, your game will
        fall into a death spiral, as each frame takes longer and longer to compute!

        For more info, see Glenn Fiedler's "Fix Your Timestep!"

        :param timestep: Length of the time step, in seconds. Passed from
        timing_settings.
        :param accumulated_time: Time passed since last const_update.
        :return: Remaining accumulated time.
        """
        while accumulated_time > timestep:
            self.const_update(timestep)
            accumulated_time -= timestep
        return accumulated_time

    def render(self, window: pygame.Surface, delta_time: float) -> None:
        """
        Main drawing phase. Used for rendering active game objects to the screen.

        :param window: The main display window.
        :param delta_time: Time passed since last frame, in seconds.
        """
        for entity in self.entity_manager.renderables:
            surface, rect = entity.render(delta_time)
            window.blit(surface, rect)

    def render_ui(self, window: pygame.Surface, delta_time: float) -> None:
        """
        Late drawing phase for UI elements. Used for rendering any elements that must
        be drawn after the main render phase, such as UI.

        :param window: The main display window.
        :param delta_time: Time passed since last frame, in seconds.
        """
        for entity in self.entity_manager.ui_elements:
            surface, rect = entity.render_ui(delta_time)
            window.blit(surface, rect)

    def patch_render(self, new_render: Callable) -> None:
        """
        Override the default render method with the supplied function.
        Supplied function must match default render signature.
        Signature is: (self: Game, window: Surface, delta_time: float)

        :param new_render: Callable matching render signature.
        """
        self._monkeypatch_method(self.render, new_render)

    def patch_render_ui(self, new_render_ui: Callable) -> None:
        """
        Override the default render_ui method with the supplied function.
        Supplied function must match default render_ui signature.
        Signature is: (self: Game, window: Surface, delta_time: float)

        :param new_render_ui: Callable matching render_ui signature.
        """
        self._monkeypatch_method(self.render_ui, new_render_ui)

    def _render_block(self, window: pygame.Surface, delta_time: float) -> None:
        """
        Calls the render functions, and updates the display.

        :param window: The main display window.
        :param delta_time: Time passed since last frame, in seconds.
        """
        self.render(window, delta_time)
        self.render_ui(window, delta_time)

        pygame.display.flip()

    def quit(self) -> None:
        """
        Ends the game loop.
        """
        self.is_running = False

    def quit_called(self) -> None:
        """
        Hook for attaching behavior to the pygame.QUIT event. By default, quits the
        game.
        """
        self.quit()

    def process_events(self, events: list[pygame.Event]) -> None:
        """
        Takes the list of events generated, and processes them.
        by default, the events are passed on to handle_event.
        Pygame.QUIT is specifically checked.

        :param events: List of events since last frame.
        """
        for event in events:
            if event.type == pygame.QUIT:
                self.quit_called()
            self.handle_event(event)

    def handle_event(self, event: pygame.Event) -> None:
        """
        Method hook for event behavior.

        Recommendation: Use https://pypi.org/project/pygame-simple-events/ for handling
        events (Shameless plug!)

        :param event: Event to be handled.
        """
        pass


class AsyncGame(Game):
    """
    Variant of Game that runs in async mode.
    Supports pygbag.
    """

    async def start_game(self):
        """
        Begins the game loop in async mode.
        Identical to Base game version, except with an asyncio sleep attached for
        thread handoff required for tools like pygbag.
        """

        accumulated_time: float = 0.0

        # Minimum duplication to get desired results.
        while self.is_running:
            accumulated_time = self._main_loop_body(accumulated_time)
            await asyncio.sleep(0)

    def main(self):
        """
        Main entry point for the game. By default, starts a thread from start_game().
        """
        self.create_window()
        asyncio.run(self.start_game())
