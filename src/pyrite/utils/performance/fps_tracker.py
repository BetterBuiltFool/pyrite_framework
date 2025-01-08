class FPSTracker(Entity):

    def __init__(self, container: Container = None, enabled=True) -> None:
        super().__init__(container, enabled)
        self.max: float = 0
        self.min: float = sys.float_info.max
        self.max_entities: int = 0
        self.max_renderables: int = 0

    def __del__(self):
        print(f"Maximum framerate: {self.max:.1f}; Minimum framerate: {self.min:.1f}")
        print(f"Maximum entities at once: {self.max_entities}")
        print(f"Maximum renderables at once: {self.max_renderables}")

    def post_update(self, delta_time: float) -> None:
        game_instance: Game = self.container

        current_fps = game_instance.clock.get_fps()

        self.max = max(current_fps, self.max)
        if current_fps > 0:  # To bypass startup lag
            self.min = min(current_fps, self.min)

        self.max_entities = max(
            self.max_entities, len(game_instance.entity_manager.entities) - 1
        )

        renderables = 0
        for layer in game_instance.renderer.renderables.values():
            renderables += len(layer)
        self.max_renderables = max(self.max_renderables, renderables)
