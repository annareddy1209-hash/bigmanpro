
import unittest
import pandas as pd

from engines.inducement import (
    detect_inducement,
    validate_data,
)


class TestInducementEngine(unittest.TestCase):

    def test_bullish_wick_only_break(self):
        data = pd.DataFrame({
            "open": [105, 103, 102],
            "high": [108, 106, 105],
            "low": [102, 99, 101],
            "close": [106, 104, 103],
        })

        result = detect_inducement(
            data,
            bos_index=0,
            inducement_level=100,
            direction="BULLISH",
        )

        self.assertTrue(result["detected"])
        self.assertEqual(result["direction"], "BULLISH")
        self.assertEqual(result["inducement_index"], 1)
        self.assertEqual(result["break_type"], "BELOW")

    def test_bearish_wick_only_break(self):
        data = pd.DataFrame({
            "open": [100, 103, 102],
            "high": [102, 111, 106],
            "low": [98, 101, 99],
            "close": [101, 105, 103],
        })

        result = detect_inducement(
            data,
            bos_index=0,
            inducement_level=110,
            direction="BEARISH",
        )

        self.assertTrue(result["detected"])
        self.assertEqual(result["direction"], "BEARISH")
        self.assertEqual(result["inducement_index"], 1)
        self.assertEqual(result["break_type"], "ABOVE")

    def test_first_qualifying_break_is_selected(self):
        data = pd.DataFrame({
            "open": [105, 104, 103, 102],
            "high": [108, 107, 106, 105],
            "low": [102, 99, 98, 97],
            "close": [106, 103, 102, 101],
        })

        result = detect_inducement(
            data,
            bos_index=0,
            inducement_level=100,
            direction="BULLISH",
        )

        self.assertEqual(result["inducement_index"], 1)

    def test_no_break_after_bos(self):
        data = pd.DataFrame({
            "open": [105, 104, 103],
            "high": [108, 107, 106],
            "low": [102, 101, 100],
            "close": [106, 103, 102],
        })

        result = detect_inducement(
            data,
            bos_index=0,
            inducement_level=99,
            direction="BULLISH",
        )

        self.assertFalse(result["detected"])
        self.assertIsNone(result["inducement_index"])

    def test_break_before_bos_is_ignored(self):
        data = pd.DataFrame({
            "open": [105, 104, 103],
            "high": [108, 107, 106],
            "low": [98, 101, 102],
            "close": [103, 105, 104],
        })

        result = detect_inducement(
            data,
            bos_index=1,
            inducement_level=100,
            direction="BULLISH",
        )

        self.assertFalse(result["detected"])

    def test_invalid_direction(self):
        data = pd.DataFrame({
            "open": [100],
            "high": [105],
            "low": [95],
            "close": [102],
        })

        with self.assertRaises(ValueError):
            detect_inducement(
                data,
                bos_index=0,
                inducement_level=98,
                direction="SIDEWAYS",
            )

    def test_invalid_bos_index(self):
        data = pd.DataFrame({
            "open": [100],
            "high": [105],
            "low": [95],
            "close": [102],
        })

        with self.assertRaises(ValueError):
            detect_inducement(
                data,
                bos_index=5,
                inducement_level=98,
                direction="BULLISH",
            )

    def test_invalid_candle_data(self):
        data = pd.DataFrame({
            "open": [100],
            "high": [90],
            "low": [95],
            "close": [102],
        })

        with self.assertRaises(ValueError):
            validate_data(data)


if __name__ == "__main__":
    unittest.main()
