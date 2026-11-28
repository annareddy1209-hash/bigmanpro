
import unittest
import pandas as pd

from engines.swing_detection import (
    detect_swing_points,
    get_latest_swings,
)


class TestSwingDetection(unittest.TestCase):

    def setUp(self):
        self.data = pd.DataFrame({
            "datetime": pd.date_range(
                "2026-11-28",
                periods=9,
                freq="15min",
            ),
            "open":  [10, 11, 12, 13, 12, 11, 10, 11, 12],
            "high":  [11, 12, 13, 16, 13, 12, 11, 12, 13],
            "low":   [9, 10, 11, 12, 10, 8, 9, 10, 11],
            "close": [10, 11, 12, 14, 11, 9, 10, 11, 12],
        })

    def test_detect_swing_high(self):
        swings = detect_swing_points(self.data)

        highs = [
            swing for swing in swings
            if swing["type"] == "swing_high"
        ]

        self.assertEqual(len(highs), 1)
        self.assertEqual(highs[0]["index"], 3)
        self.assertEqual(highs[0]["price"], 16)

    def test_detect_swing_low(self):
        swings = detect_swing_points(self.data)

        lows = [
            swing for swing in swings
            if swing["type"] == "swing_low"
        ]

        self.assertEqual(len(lows), 1)
        self.assertEqual(lows[0]["index"], 5)
        self.assertEqual(lows[0]["price"], 8)

    def test_confirmation_index(self):
        swings = detect_swing_points(self.data)

        for swing in swings:
            self.assertEqual(
                swing["confirmation_index"],
                swing["index"] + 2,
            )

    def test_latest_swings(self):
        result = get_latest_swings(self.data)

        self.assertIsNotNone(
            result["latest_swing_high"]
        )

        self.assertIsNotNone(
            result["latest_swing_low"]
        )

        self.assertEqual(result["total_swings"], 2)

    def test_invalid_left_bars(self):
        with self.assertRaises(ValueError):
            detect_swing_points(
                self.data,
                left_bars=0,
            )

    def test_invalid_right_bars(self):
        with self.assertRaises(ValueError):
            detect_swing_points(
                self.data,
                right_bars=0,
            )

    def test_missing_columns(self):
        with self.assertRaises(ValueError):
            detect_swing_points(
                self.data.drop(columns=["high"])
            )

    def test_empty_data(self):
        with self.assertRaises(ValueError):
            detect_swing_points(
                self.data.iloc[0:0]
            )


if __name__ == "__main__":
    unittest.main()
