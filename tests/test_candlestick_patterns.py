
import unittest
import pandas as pd

from engines.candlestick_patterns import (
    detect_candlestick_patterns,
    validate_candles,
)


class TestCandlestickPatterns(unittest.TestCase):

    def make_data(self, candles):
        return pd.DataFrame(
            candles,
            columns=["open", "high", "low", "close"],
        )

    def test_hammer(self):
        data = self.make_data([
            [10, 11.2, 7, 11],
        ])

        result = detect_candlestick_patterns(data)

        self.assertIn("HAMMER", result["patterns"])

    def test_shooting_star(self):
        data = self.make_data([
            [10.2, 14, 9.8, 10],
        ])

        result = detect_candlestick_patterns(data)

        self.assertIn("SHOOTING_STAR", result["patterns"])

    def test_doji(self):
        data = self.make_data([
            [10, 11, 9, 10.05],
        ])

        result = detect_candlestick_patterns(data)

        self.assertIn("DOJI", result["patterns"])

    def test_bullish_engulfing(self):
        data = self.make_data([
            [11, 11.2, 9.8, 10],
            [9.7, 11.5, 9.5, 11.3],
        ])

        result = detect_candlestick_patterns(data)

        self.assertIn(
            "BULLISH_ENGULFING",
            result["patterns"],
        )

    def test_bearish_engulfing(self):
        data = self.make_data([
            [10, 11.2, 9.8, 11],
            [11.3, 11.5, 9.5, 9.7],
        ])

        result = detect_candlestick_patterns(data)

        self.assertIn(
            "BEARISH_ENGULFING",
            result["patterns"],
        )

    def test_three_white_soldiers(self):
        data = self.make_data([
            [10, 11.2, 9.8, 11],
            [10.8, 12.2, 10.6, 12],
            [11.8, 13.2, 11.6, 13],
        ])

        result = detect_candlestick_patterns(data)

        self.assertIn(
            "THREE_WHITE_SOLDIERS",
            result["patterns"],
        )

    def test_three_black_crows(self):
        data = self.make_data([
            [13, 13.2, 11.8, 12],
            [12.2, 12.4, 10.8, 11],
            [11.2, 11.4, 9.8, 10],
        ])

        result = detect_candlestick_patterns(data)

        self.assertIn(
            "THREE_BLACK_CROWS",
            result["patterns"],
        )

    def test_no_pattern(self):
        data = self.make_data([
            [10, 10.5, 9.5, 10.2],
        ])

        result = detect_candlestick_patterns(data)

        self.assertFalse(result["detected"])

    def test_custom_index(self):
        data = self.make_data([
            [10, 10.5, 9.5, 10.2],
            [10, 11.2, 7, 11],
        ])

        result = detect_candlestick_patterns(
            data,
            index=1,
        )

        self.assertEqual(result["index"], 1)
        self.assertIn("HAMMER", result["patterns"])

    def test_invalid_index(self):
        data = self.make_data([
            [10, 11, 9, 10.5],
        ])

        with self.assertRaises(ValueError):
            detect_candlestick_patterns(data, index=5)

    def test_invalid_candle_data(self):
        data = self.make_data([
            [100, 90, 95, 102],
        ])

        with self.assertRaises(ValueError):
            validate_candles(data)


if __name__ == "__main__":
    unittest.main()
