from __future__ import annotations

import asyncio
import logging
from typing import Self, TYPE_CHECKING

from pygame import Rect

from .core.display_settings import DisplaySettings
from .core.entity_manager import EntityManager
from .core.game_data import GameData
from .core.render_system import RenderSystem, RenderManager
from .core.rate_settings import RateSettings
from .core.system_manager import SystemManager

from pyrite._camera.camera import Camera
from pyrite._rendering.ortho_projection import OrthoProjection
from pyrite._rendering.viewport import Viewport
from pyrite._services.camera_service import CameraServiceProvider as CameraService
from ._transform import transform_system
from .utils import threading

if TYPE_CHECKING:
    from types import TracebackType
    from .types.system import System


import pygame

logger = logging.getLogger(__name__)

_active_instance = None


def get_game_instance() -> Game | None:
    """
    Gets the running game instance, if it exists.
    """
    return _active_instance


def set_game_instance(instance: Game):
    """
    Sets the game instance to the one passed.
    """
    global _active_instance
    _active_instance = instance


class Game:
    """
    Base Game object to serve as a parent for your game.
    Holds onto data required for generating the window and performing the main loop.
    Only one game instance may be running at a time. Attempting to start a new instance
    will stop the previous instance.
    """

    def __new__(cls, *args, **kwds) -> Self:
        active_instance = get_game_instance()
        if active_instance is not None:
            active_instance.is_running = False
            logger.info(
                f"Stopping {active_instance}, only one game may be running at a time."
            )
        logger.info("Starting new game instance.")
        active_instance = super().__new__(cls)
        set_game_instance(active_instance)
        return active_instance

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

        # Ensures the threading service is properly initialized.
        self.init_threader()

        # Extract various settings and game data from keyword arguments.
        # Creates defaults if none are provided.
        self.display_settings = DisplaySettings.get_display_settings(**kwds)
        self.game_data = GameData.get_game_data(**kwds)
        self.rate_settings = RateSettings.get_rate_settings(**kwds)

        # Entity manager is responsible for holding and updating all entities.
        # Renderer is responsible for holding and drawing all renderables.
        # Both have a default version that will be spawned if none is provided.
        self.entity_manager: EntityManager = EntityManager.get_entity_manager(**kwds)
        self.render_manager = RenderManager.get_render_manager(**kwds)
        self.renderer = RenderSystem.get_renderer(**kwds)
        self.system_manager = SystemManager.get_system_manager(**kwds)

        self.starting_systems: list[type[System]] = [
            transform_system.get_default_transform_system_type()
        ]

        # Create a placeholder for the window, and the create the actual window
        self.window: pygame.Surface
        self.create_window()

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

    def init_threader(self):
        threading._set_regular_mode()

    def create_window(self):
        """
        Generates a window from current display settings.
        Updates the icon, if possible.
        The game's window and display settings are updated to reflect the new window.
        """
        if self.game_data.icon is not None:
            pygame.display.set_icon(self.game_data.icon)
        self.window, self.display_settings = DisplaySettings.create_window(
            self.display_settings
        )
        # Ensure we have a default camera in case there are no others.
        default_camera = Camera(
            OrthoProjection(Rect(0, 0, *self.window.size)), enabled=False
        )
        CameraService._default_camera = default_camera
        # Update the default camera so that it captures the new display.
        CameraService.update_default_camera(self.window.size)

        # Update the viewports so they are sized correctly
        Viewport.update_viewports(self.window.size)

    def add_system(self, system_type: type[System]):
        self.starting_systems.append(system_type)

    def start_systems(self):
        """
        Initializes any systems that are indicated to be required when the game starts.
        """
        for system in self.starting_systems:
            system()

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

        self.start_systems()

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
            self.rate_settings.fps_cap, accumulated_time
        )

        # This will ensure new entities are processed properly for the new frame.
        self.entity_manager.flush_buffer()
        self.system_manager.prepare_systems()

        self.process_events(pygame.event.get())

        if self.rate_settings.tick_rate > 0:
            accumulated_time = self._fixed_update_block(
                self.rate_settings.fixed_timestep, accumulated_time
            )

        self._update_block(delta_time)

        if not (caption := self.game_data.caption):
            caption = self.game_data.title
        pygame.display.set_caption(caption)
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

    def pre_update(self, delta_time: float) -> None:
        """
        Early update function. Used for game logic that needs to run _before_ the main
        update phase.

        :param delta_time: Actual time passed since last frame, in seconds.
        """
        pass

    def update(self, delta_time: float) -> None:
        """
        Main update function. Used for coordinating most of the game state changes
        required.

        :param delta_time: Actual time passed since last frame, in seconds.
        """
        pass

    def post_update(self, delta_time: float) -> None:
        """
        Late update function. Used for game logic that needs to run _after_ the main
        update phase.

        :param delta_time: Actual time passed since last frame, in seconds.
        """
        pass

    def const_update(self, timestep: float) -> None:
        """
        Update function that runs at a constant rate. Useful for anything that is
        sensitive to variations in frame time, such as physics.

        This is a basic, naïve implementation of a fixed timestep, and can be a bit
        jittery, especially when the tick rate and frame rate are not multiples of
        eachother.

        For more info, see Glenn Fiedler's "Fix Your Timestep!"

        :param timestep: Simulated time passed since last update. Passed in from the
        game's rate_settings.
        """
        pass

    def _update_block(self, delta_time: float) -> None:
        """
        Calls all of the update phases, in order.

        :param delta_time: Actual time passed since last frame, in seconds.
        """

        self.pre_update(delta_time)
        self.system_manager.pre_update(delta_time)
        self.entity_manager.pre_update(delta_time)
        self.update(delta_time)
        self.system_manager.update(delta_time)
        self.entity_manager.update(delta_time)
        self.post_update(delta_time)
        self.system_manager.post_update(delta_time)
        self.entity_manager.post_update(delta_time)

    def _fixed_update_block(self, timestep: float, accumulated_time: float) -> float:
        """
        Runs const_update so long as accumulated time is greater than the timestep.

        CAUTION: If const_update takes longer to run than the timestep, your game will
        fall into a death spiral, as each frame takes longer and longer to compute!

        For more info, see Glenn Fiedler's "Fix Your Timestep!"

        :param timestep: Length of the time step, in seconds. Passed from
        rate_settings.
        :param accumulated_time: Time passed since last const_update.
        :return: Remaining accumulated time.
        """
        while accumulated_time > timestep:
            self.const_update(timestep)
            self.system_manager.const_update(timestep)
            self.entity_manager.const_update(timestep)
            accumulated_time -= timestep
        return accumulated_time

    def render(self, window: pygame.Surface, delta_time: float) -> None:
        """
        Main drawing phase. Used for rendering active game objects to the screen.

        :param window: The main display window.
        :param delta_time: Time passed since last frame, in seconds.
        """
        pass

    def _render_block(self, window: pygame.Surface, delta_time: float) -> None:
        """
        Calls the render functions, and updates the display.

        :param window: The main display window.
        :param delta_time: Time passed since last frame, in seconds.
        """
        # Finalize any systems
        self.system_manager.pre_render(delta_time)

        # Redundant if no cameras, but cameras could cause this to be needed.
        window.fill(pygame.Color("black"))  # TODO Make this changeable

        render_queue = self.render_manager.generate_render_queue()
        self.renderer.render(self.window, delta_time, render_queue)

        self.render(window, delta_time)

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
        by default, the events are passed on to handle_event and the entity manager.
        Pygame.QUIT is specifically checked.

        :param events: List of events since last frame.
        """
        for event in events:
            if event.type == pygame.QUIT:
                self.quit_called()

            self.entity_manager.handle_event(event)
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

    async def start_game_async(self):
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

    def init_threader(self):
        threading._set_asyncio_mode()

    def main(self):
        """
        Main entry point for the game. By default, starts a thread from start_game().
        """
        self.create_window()
        asyncio.run(self.start_game_async())
