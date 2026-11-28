
import unittest
import pandas as pd
from unittest.mock import patch

from engines.market_bias import (
    analyze_market_bias,
    get_market_bias_status,
)


class TestMarketBias(unittest.TestCase):

    def setUp(self):
        self.bullish_data = pd.DataFrame({
            "datetime": pd.date_range(
                "2026-11-28",
                periods=9,
                freq="15min",
            ),
            "open":  [9.5, 11, 9, 8, 11, 13, 11, 10, 10.5],
            "high":  [10, 12, 11, 10, 14, 15, 13, 12, 11],
            "low":   [9, 10, 8, 7, 9, 11, 10, 9, 10],
            "close": [9.8, 11.5, 9.5, 8.5, 12, 14, 11.5, 10.5, 10.8],
        })

    def test_bullish_market_bias(self):
        result = analyze_market_bias(
            self.bullish_data,
            left_bars=1,
            right_bars=1,
        )

        self.assertEqual(result["bias"], "BULLISH")
        self.assertEqual(result["status"], "STRUCTURE_ALIGNED")
        self.assertTrue(result["higher_high"])
        self.assertTrue(result["higher_low"])

    @patch("engines.market_bias.detect_swing_points")
    def test_bearish_market_bias(self, mock_swings):
        mock_swings.return_value = [
            {"index": 1, "price": 15, "type": "swing_high"},
            {"index": 3, "price": 12, "type": "swing_low"},
            {"index": 5, "price": 13, "type": "swing_high"},
            {"index": 7, "price": 9, "type": "swing_low"},
        ]

        result = analyze_market_bias(self.bullish_data)

        self.assertEqual(result["bias"], "BEARISH")
        self.assertTrue(result["lower_high"])
        self.assertTrue(result["lower_low"])

    @patch("engines.market_bias.detect_swing_points")
    def test_mixed_structure_is_neutral(self, mock_swings):
        mock_swings.return_value = [
            {"index": 1, "price": 12, "type": "swing_high"},
            {"index": 3, "price": 8, "type": "swing_low"},
            {"index": 5, "price": 15, "type": "swing_high"},
            {"index": 7, "price": 6, "type": "swing_low"},
        ]

        result = analyze_market_bias(self.bullish_data)

        self.assertEqual(result["bias"], "NEUTRAL")
        self.assertEqual(result["status"], "MIXED_STRUCTURE")

    @patch("engines.market_bias.detect_swing_points")
    def test_insufficient_swings_is_neutral(self, mock_swings):
        mock_swings.return_value = [
            {"index": 3, "price": 12, "type": "swing_high"},
            {"index": 5, "price": 8, "type": "swing_low"},
        ]

        result = analyze_market_bias(self.bullish_data)

        self.assertEqual(result["bias"], "NEUTRAL")
        self.assertEqual(
            result["status"],
            "INSUFFICIENT_STRUCTURE",
        )

    @patch("engines.market_bias.detect_swing_points")
    def test_no_swings_is_neutral(self, mock_swings):
        mock_swings.return_value = []

        result = analyze_market_bias(self.bullish_data)

        self.assertEqual(result["bias"], "NEUTRAL")
        self.assertEqual(result["confirmed_swing_count"], 0)

    def test_engine_status(self):
        result = get_market_bias_status()

        self.assertEqual(
            result["engine"],
            "Market Bias Engine",
        )

        self.assertTrue(
            result["uses_confirmed_swings"]
        )

        self.assertFalse(
            result["generates_trade_signals"]
        )


if __name__ == "__main__":
    unittest.main()
