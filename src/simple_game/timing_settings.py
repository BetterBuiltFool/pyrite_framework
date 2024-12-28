from __future__ import annotations

import logging
import typing

logger = logging.getLogger(__name__)
MAX_TICK_RATE = 120


class TimingSettings:
    def __init__(self, fps_cap: int = 0, tick_rate: float = 20) -> None:
        """
        Creates a new Timings object, which hold framerate data for a Game object.

        :param fps_cap: Maximum frame rate, in frames per second, defaults to 0.
        0 uncaps framerate.
        :param tick_rate: Number of times per second that const_update runs,
        defaults to 20. Setting to 0 disables const_update.
        """
        if fps_cap < 0:
            fps_cap = 0
        self._fps_cap = fps_cap
        if tick_rate < 0:
            tick_rate = 0
        self._tick_rate = tick_rate
        self._fixed_timestep: float = tick_rate / 1000 if tick_rate > 0 else 1000

    @property
    def fps_cap(self) -> int:
        """
        Maximum frame rate, in frames per second. Must be positive.

        Setting to 0 will uncap the framerate.
        """
        return self._fps_cap

    @fps_cap.setter
    def fps_cap(self, target: int) -> None:
        if target < 0:
            raise ValueError("FPS must be positive.")
        self._fps_cap = target

    @property
    def tick_rate(self) -> float:
        """
        Number of times per second that the constant update phase runs, default 20.
        Timestep length is calculated from this number.

        Must be a positive value.

        Setting to 0 disables const_update
        """
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
        """
        Length of the timestep between constant updates. Setting this value
        recalculates tick_rate.

        Must be greater than 0.
        """
        return self._fixed_timestep

    @fixed_timestep.setter
    def fixed_timestep(self, target: float) -> None:
        if target <= 0:
            raise ValueError("Timestep must be greater than zero.")
        self._fixed_timestep = target
        self._tick_rate = target * 1000

    @staticmethod
    def get_timing_settings(**kwds) -> TimingSettings:
        """
        Creates a TimingSettings object from external arguments.
        Used for generating timing settings from arguments passed into Game init.
        """
        timing_data: TimingSettings | None = kwds.get("timing_data", None)
        if timing_data is None:
            # Creates a new TimingSettings if one hasn't been passed.
            keys: set = {"fps_cap", "tick_rate", "fixed_timestep"}
            params: dict = {key: kwds[key] for key in keys if key in kwds}
            timing_data = TimingSettings(**params)
        return typing.cast(TimingSettings, timing_data)
