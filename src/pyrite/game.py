from abc import ABC, abstractmethod
import asyncio

from src.pyrite.timing_settings import TimingSettings
from src.pyrite.display_settings import DisplaySettings

import pygame


class Game(ABC):
    """
    Base Game object to serve as a parent for your game.
    Holds onto data required for generating the window and performing the main loop.
    """

    def __init__(self, **kwds) -> None:

        suppress_init = kwds.get("suppress_init", False)
        self.debug_mode = kwds.get("debug_mode", False)

        if not suppress_init:
            pygame.init()

        self.is_running = True
        self.clock = pygame.time.Clock()
        self.timing_settings = TimingSettings.get_timing_settings(**kwds)
        display_settings = DisplaySettings.get_display_settings(**kwds)
        self.window, self.display_settings = DisplaySettings.create_window(
            display_settings
        )

    def main(self):
        """
        The main entry point for the game. By default, calls start_game(), but can be
        overridden to have more complex starting logic.

        For example, a function could be called to create a special early loop for
        loading in resources before calling the main game loop.
        """
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

    def _update_block(self, delta_time: float) -> None:
        """
        Calls all of the update phases, in order.

        :param delta_time: Actual time passed since last frame, in seconds.
        """
        self.pre_update(delta_time)
        self.update(delta_time)
        self.post_update(delta_time)

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
        pass

    def render(self, window: pygame.Surface, delta_time: float) -> None:
        """
        Main drawing phase. Used for rendering active game objects to the screen.

        :param window: The main display window.
        :param delta_time: Time passed since last frame, in seconds.
        """
        pass

    def render_ui(self, window: pygame.Surface, delta_time: float) -> None:
        """
        Late drawing phase for UI elements. Used for rendering any elements that must
        be drawn after the main render phase, such as UI.

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

    @abstractmethod
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
        asyncio.run(self.start_game())
