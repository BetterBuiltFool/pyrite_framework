from __future__ import annotations

import logging
import typing

import pyrite.time

logger = logging.getLogger(__name__)

MAX_TICK_RATE_WARNING = 120.0
"""
Maximum tick rate. Setting tick rate above this value will cause a warning to be logged.
"""


def set_max_tickrate(value: float):
    """
    Adjusts the value

    :param value: _description_
    """
    if value <= 0:
        logger.warning(
            "Setting MAX_TICK_RATE_WARNING below 1 will cause the warning to apply to "
            "all valid tickrates."
        )
    global MAX_TICK_RATE_WARNING
    MAX_TICK_RATE_WARNING = value


class RateSettings:
    def __init__(self, fps_cap: int = 0, tick_rate: float = 20) -> None:
        """
        Creates a new Rates object, which hold framerate data for a Game object.

        :param fps_cap: Maximum frame rate, in frames per second, defaults to 0.
        0 uncaps framerate.
        :param tick_rate: Number of times per second that const_update runs,
        defaults to 20. Setting to 0 disables const_update.
        """
        if fps_cap < 0:
            fps_cap = 0
        self._fps_cap: int = fps_cap
        if tick_rate < 0:
            tick_rate = 0
        self._tick_rate: float = tick_rate
        # Setting fixed timestep to -1 if timestep is 0 in case it gets referenced
        # without checking tickrate.
        self._fixed_timestep: float = 1 / tick_rate if tick_rate > 0 else -1

        self._set_fixed_time_step(self._fixed_timestep)

    @property
    def fps_cap(self) -> int:
        """
        Maximum frame rate, in frames per second. Must be positive.

        Setting to 0 will uncap the framerate.
        """
        return self._fps_cap

    @fps_cap.setter
    def fps_cap(self, fps_cap: int) -> None:
        if fps_cap < 0:
            raise ValueError("FPS must be positive.")
        self._fps_cap = fps_cap

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
    def tick_rate(self, tick_rate: float) -> None:
        if tick_rate < 0:
            logger.warning(
                "Tick rates less than 0 are not allowed. Setting to 0 (disables "
                "const_update)"
            )
            tick_rate = 0
        if tick_rate > MAX_TICK_RATE_WARNING:
            logger.warning("High tick rates may cause instability. Use with caution.")
        if self._tick_rate == 0 and tick_rate != 0:
            logger.info(f"Tick rate set to '{tick_rate}'. 'const_update' is enabled.")
        self._tick_rate = tick_rate
        if tick_rate != 0:
            self._fixed_timestep = 1 / tick_rate
        else:
            self._fixed_timestep = -1
            logger.info("Tick rate set to '0'. 'const_update' is disabled.")

        self._set_fixed_time_step(self._fixed_timestep)

    @property
    def fixed_timestep(self) -> float:
        """
        Length of the timestep between constant updates. Setting this value
        recalculates tick_rate.

        A returned value of -1 indicates tick_rate is '0' and const_update is disabled.

        :raises ValueError: Errors when set to zero or less. Tick rate must be disabled
        by setting tick_rate to 0.
        """
        return self._fixed_timestep

    @fixed_timestep.setter
    def fixed_timestep(self, fixed_timestep: float) -> None:
        if fixed_timestep <= 0:
            raise ValueError("Timestep must be greater than zero.")
        self._fixed_timestep = fixed_timestep
        self._tick_rate = 1 / fixed_timestep

        self._set_fixed_time_step(self._fixed_timestep)

    @staticmethod
    def _set_fixed_time_step(timestep: float) -> None:
        pyrite.time.DeltaTime._update_fixed(timestep)

    @staticmethod
    def get_rate_settings(**kwds) -> RateSettings:
        """
        Creates a RateSettings object from external arguments.
        Used for generating rate settings from arguments passed into Game init.
        """
        rate_data: RateSettings | None = kwds.get("rate_settings", None)
        if rate_data is None:
            # Creates a new RateSettings if one hasn't been passed.
            keys: set = {"fps_cap", "tick_rate", "fixed_timestep"}
            params: dict = {key: kwds[key] for key in keys if key in kwds}
            rate_data = RateSettings(**params)
        return typing.cast(RateSettings, rate_data)
