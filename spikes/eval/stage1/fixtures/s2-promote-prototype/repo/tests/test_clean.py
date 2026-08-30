"""Tests for lib.clean — unittest style used across this repo."""
import unittest

from lib.clean import normalize_tag, split_pair


class NormalizeTagTest(unittest.TestCase):
    def test_lowercases_and_trims(self):
        self.assertEqual(normalize_tag("  Ops "), "ops")

    def test_rejects_empty(self):
        with self.assertRaises(ValueError):
            normalize_tag("   ")


class SplitPairTest(unittest.TestCase):
    def test_splits_once(self):
        self.assertEqual(split_pair("a:b:c"), ("a", "b:c"))

    def test_rejects_missing_separator(self):
        with self.assertRaises(ValueError):
            split_pair("abc")


if __name__ == "__main__":
    unittest.main()
