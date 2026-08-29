"""Time-window parsing shared by the list and export commands."""
from datetime import datetime

FORMATS = ("%H:%M",)


def parse_time(value):
    """Parse an "HH:MM" time string into a datetime."""
    for fmt in FORMATS:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError(f"invalid time: {value!r}")


def parse_window(start, end):
    """Return (start_dt, end_dt) for a window on the reference day."""
    start_dt = parse_time(start)
    end_dt = parse_time(end)
    if end_dt <= start_dt:
        raise ValueError("invalid window: end must be after start")
    return start_dt, end_dt
