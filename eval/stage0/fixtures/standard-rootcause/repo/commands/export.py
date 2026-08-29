"""Export windows to the nightly scheduler feed.

Rows the parser rejects are not schedulable and are skipped.
"""
from lib.windows import parse_window


def export_rows(rows):
    """Return scheduler-feed dicts for each parseable (label, start, end) row."""
    exported = []
    for label, start, end in rows:
        try:
            start_dt, end_dt = parse_window(start, end)
        except ValueError:
            continue
        exported.append(
            {
                "label": label,
                "start": start_dt.isoformat(),
                "end": end_dt.isoformat(),
            }
        )
    return exported
