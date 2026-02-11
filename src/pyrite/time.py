class DeltaTime:
    """
    Static class that provides methods for interacting with per-frame time variations.
    """

    _dt: float = 0
    _fxt: float = 0

    @staticmethod
    def _update_dt(delta_time: float) -> None:
        DeltaTime._dt = delta_time

    @staticmethod
    def _update_fixed(step: float) -> None:
        DeltaTime._fxt = step

    @staticmethod
    def seconds() -> float:
        """
        Returns the time since the previous frame, in seconds.
        """
        return DeltaTime._dt / 1000

    @staticmethod
    def milliseconds() -> float:
        """
        Returns the time since the previous frame, in milliseconds.
        """
        return DeltaTime._dt

    @staticmethod
    def fixed_step_seconds() -> float:
        """
        Returns the length of the fixed step used by const_update, in seconds.
        """
        return DeltaTime._fxt / 1000

    @staticmethod
    def fixed_step_milliseconds() -> float:
        """
        Returns the length of the fixed step used by const_update, in milliseconds.
        """
        return DeltaTime._fxt
