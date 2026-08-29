import unittest

from commands.list import list_windows


class TestList(unittest.TestCase):
    def test_same_day_window(self):
        self.assertEqual(
            list_windows([("backup", "09:00", "11:00")])[0],
            "backup: 09:00-11:00 (120 min)",
        )

    def test_overnight_window_listed(self):
        result = list_windows([("reindex", "22:00", "06:00")])[0]
        self.assertTrue(result.startswith("reindex: 22:00-06:00 (480 min)"), result)


if __name__ == "__main__":
    unittest.main()
