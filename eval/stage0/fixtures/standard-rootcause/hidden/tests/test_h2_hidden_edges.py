import unittest
from datetime import timedelta

from lib.windows import parse_window


class TestWindowEdges(unittest.TestCase):
    def test_cross_midnight(self):
        start, end = parse_window("22:00", "06:00")
        self.assertEqual((start.hour, end.hour), (22, 6))
        self.assertEqual(end - start, timedelta(hours=8))

    def test_end_at_24_00(self):
        start, end = parse_window("20:00", "24:00")
        self.assertEqual(end - start, timedelta(hours=4))


# Deliberately NOT asserted (underdetermined by issue #7 — Stage 0
# finding #2): equal start/end semantics and 00:00->24:00 full-day windows.
# Observed legitimate readings across systems: reject, zero-length, or
# 24-hour window; all three are consistent with the stated requirements.


if __name__ == "__main__":
    unittest.main()
