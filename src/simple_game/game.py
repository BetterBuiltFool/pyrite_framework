from abc import ABC, abstractmethod
from typing import cast

from src.simple_game.timing_settings import TimingSettings
from src.simple_game.display_settings import DisplaySettings

import pygame


class Game(ABC):

    def __init__(self, **kwds) -> None:

        suppress_init = kwds.get("suppress_init", False)
        self.debug_mode = kwds.get("debug_mode", False)

        if not suppress_init:
            pygame.init()

        self.is_running = True
        self.clock = pygame.time.Clock()
        self.timings = self._get_timings(**kwds)
        display_settings = DisplaySettings.get_display_settings(**kwds)
        self.window, self.display_settings = DisplaySettings.create_window(
            display_settings
        )

    def main(self) -> None:

        accumulated_time: float = 0.0

        while self.is_running:

            delta_time = self.clock.tick(self.timings.fps_cap) / 1000
            accumulated_time += delta_time

            self.handle_events(pygame.event.get())

            timestep = self.timings.fixed_timestep

            while accumulated_time > timestep and self.timings.tick_rate > 0:
                self.const_update(timestep)
                accumulated_time -= timestep

            self.pre_update(delta_time)
            self.update(delta_time)
            self.post_update(delta_time)

            self.render(self.window, delta_time)
            self.render_ui(self.window, delta_time)

            pygame.display.flip()

    def start_game(self):
        self.main()

    def pre_update(self, delta_time: float) -> None:
        pass

    def update(self, delta_time: float) -> None:
        pass

    def post_update(self, delta_time: float) -> None:
        pass

    def const_update(self, delta_time: float) -> None:
        pass

    def render(self, window: pygame.Surface, delta_time: float) -> None:
        pass

    def render_ui(self, window: pygame.Surface, delta_time: float) -> None:
        pass

    def quit(self) -> None:
        self.is_running = False

    def quit_called(self) -> None:
        self.quit()

    def handle_events(self, events: list[pygame.Event]) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                self.quit_called()
            self.handle_event(event)

    @abstractmethod
    def handle_event(self, event: pygame.Event) -> None:
        pass

    def _get_timings(self, **kwds) -> TimingSettings:
        timing_data: TimingSettings | None = kwds.get("framerate_data", None)
        if timing_data is None:
            # Creates a new framerate data if one hasn't been passed.
            timing_data = TimingSettings()
            if (fps_cap := kwds.get("fps_cap", None)) is not None:
                timing_data.fps_cap = fps_cap
            if (tick_rate := kwds.get("tick_rate", None)) is not None:
                timing_data.tick_rate = tick_rate
            if (timestep := kwds.get("fixed_timestep", None)) is not None:
                timing_data.fixed_timestep = timestep
        return cast(TimingSettings, timing_data)
