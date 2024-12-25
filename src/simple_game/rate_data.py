import logging

logger = logging.getLogger(__name__)
MAX_TICK_RATE = 120


class FramerateData:
    def __init__(self, fps_cap: int = 0, tick_rate: float = 20) -> None:
        if fps_cap < 0:
            fps_cap = 0
        self._fps_cap = fps_cap
        if tick_rate < 0:
            tick_rate = 0
        self._tick_rate = tick_rate
        self._fixed_timestep: float = tick_rate / 1000 if tick_rate > 0 else 1000

    @property
    def tick_rate(self) -> float:
        return self._tick_rate

    @tick_rate.setter
    def tick_rate(self, target: float) -> None:
        if target < 0:
            logger.warning(
                "Tick rates less than 0 are not allowed. Setting to 0 (disables "
                "const_update)"
            )
            target = 0
        if target > MAX_TICK_RATE:
            logger.warning("High tick rates may cause instability. Use with caution.")
        self._tick_rate = target
        if target != 0:
            self._fixed_timestep = target / 1000

    @property
    def fixed_timestep(self) -> float:
        return self._fixed_timestep

    @fixed_timestep.setter
    def fixed_timestep(self, target: float) -> None:
        if target <= 0:
            raise ValueError("Timestep must be greater than zero.")
        self._fixed_timestep = target
        self._tick_rate = target * 1000
