from abc import ABC, abstractmethod

import pygame


class Game(ABC):

    def __init__(self) -> None:

        pygame.init()

        self.is_running = True
        self.window: pygame.Surface
        self.clock = pygame.time.Clock()

    def main(self) -> None:

        accumulated_time: float = 0.0
        fixed_timestep_milliseconds: float = 999999.0

        while self.is_running:

            delta_time = self.clock.tick() / 1000
            accumulated_time += delta_time

            self.handle_events(pygame.event.get())

            while accumulated_time > fixed_timestep_milliseconds:
                self.const_update(fixed_timestep_milliseconds)
                accumulated_time -= fixed_timestep_milliseconds

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
