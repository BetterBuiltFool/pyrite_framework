_dt: float = 0
_fxt: float = 0


def delta_time() -> float:
    """
    Returns the time passed since the previous frame.
    """
    return _dt


def fixed_time_step() -> float:
    """
    Returns the length of the fixed time step used in const_update.
    """
    return _fxt
