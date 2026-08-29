"""List scheduled windows for the day."""
from lib.windows import parse_window


def list_windows(rows):
    """Render one line per (label, start, end) row."""
    out = []
    for label, start, end in rows:
        try:
            start_dt, end_dt = parse_window(start, end)
        except ValueError:
            out.append(f"{label}: invalid window")
            continue
        minutes = int((end_dt - start_dt).total_seconds() // 60)
        out.append(
            f"{label}: {start_dt.strftime('%H:%M')}-{end_dt.strftime('%H:%M')} ({minutes} min)"
        )
    return out
