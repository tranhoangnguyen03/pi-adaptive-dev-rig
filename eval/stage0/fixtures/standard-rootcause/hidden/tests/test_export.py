import unittest

from commands.export import export_rows


class TestExport(unittest.TestCase):
    def test_overnight_rows_retained(self):
        rows = export_rows([("reindex", "22:00", "06:00")])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["start"][11:16], "22:00")
        self.assertEqual(rows[0]["end"][11:16], "06:00")

    def test_24_00_rows_retained(self):
        rows = export_rows([("audit", "20:00", "24:00")])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["end"][11:16], "00:00")

    def test_same_day_rows_unchanged(self):
        rows = export_rows([("backup", "09:00", "11:00")])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["start"][11:16], "09:00")


if __name__ == "__main__":
    unittest.main()
