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

    def test_full_day_from_midnight(self):
        start, end = parse_window("00:00", "24:00")
        self.assertEqual(end - start, timedelta(hours=24))

    def test_equal_start_end_is_zero_length(self):
        start, end = parse_window("09:00", "09:00")
        self.assertEqual(end - start, timedelta(0))


if __name__ == "__main__":
    unittest.main()
