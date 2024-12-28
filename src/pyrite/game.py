from abc import ABC, abstractmethod

from src.pyrite.timing_settings import TimingSettings
from src.pyrite.display_settings import DisplaySettings

import pygame


class Game(ABC):

    def __init__(self, **kwds) -> None:

        suppress_init = kwds.get("suppress_init", False)
        self.debug_mode = kwds.get("debug_mode", False)

        if not suppress_init:
            pygame.init()

        self.is_running = True
        self.clock = pygame.time.Clock()
        self.timings = TimingSettings.get_timing_settings(**kwds)
        display_settings = DisplaySettings.get_display_settings(**kwds)
        self.window, self.display_settings = DisplaySettings.create_window(
            display_settings
        )

    def main(self) -> None:

        accumulated_time: float = 0.0

        while self.is_running:

            delta_time, accumulated_time = self._get_frame_time(
                self.timings.fps_cap, accumulated_time
            )

            self.handle_events(pygame.event.get())

            if self.timings.tick_rate > 0:
                accumulated_time = self._fixed_update_block(
                    self.timings.fixed_timestep, accumulated_time
                )

            self._update_block(delta_time)

            self._render_block(self.window, delta_time)

    def start_game(self):
        self.main()

    def _get_frame_time(
        self, fps_cap: int, accumulated_time: float = 0
    ) -> tuple[float, float]:
        delta_time = self.clock.tick(fps_cap) / 1000
        accumulated_time += delta_time
        return (delta_time, accumulated_time)

    def pre_update(self, delta_time: float) -> None:
        pass

    def update(self, delta_time: float) -> None:
        pass

    def post_update(self, delta_time: float) -> None:
        pass

    def _fixed_update_block(self, timestep: float, accumulated_time: float) -> float:
        while accumulated_time > timestep:
            self.const_update(timestep)
            accumulated_time -= timestep
        return accumulated_time

    def _update_block(self, delta_time: float) -> None:
        self.pre_update(delta_time)
        self.update(delta_time)
        self.post_update(delta_time)

    def const_update(self, delta_time: float) -> None:
        pass

    def render(self, window: pygame.Surface, delta_time: float) -> None:
        pass

    def render_ui(self, window: pygame.Surface, delta_time: float) -> None:
        pass

    def _render_block(self, window: pygame.Surface, delta_time: float) -> None:
        self.render(window, delta_time)
        self.render_ui(window, delta_time)

        pygame.display.flip()

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
