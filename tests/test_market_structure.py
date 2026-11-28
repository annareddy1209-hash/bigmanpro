
import unittest
import pandas as pd

from engines.market_structure import (
    is_valid_pullback,
    calculate_retracement_percent,
    get_confirmed_structure_levels,
    confirm_bos,
    confirm_choch,
    evaluate_structure_event,
)


class TestMarketStructure(unittest.TestCase):

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

    # PULLBACK VALIDATION

    def test_pullback_above_40_percent(self):
        self.assertTrue(is_valid_pullback(45))

    def test_pullback_exactly_40_percent(self):
        self.assertTrue(is_valid_pullback(40))

    def test_pullback_below_40_percent(self):
        self.assertFalse(is_valid_pullback(35))

    def test_invalid_pullback_value(self):
        self.assertFalse(is_valid_pullback(-5))
        self.assertFalse(is_valid_pullback(110))
        self.assertFalse(is_valid_pullback(None))

    def test_calculate_bullish_retracement(self):
        result = calculate_retracement_percent(
            100, 120, 108, "bullish"
        )
        self.assertAlmostEqual(result, 60.0)

    def test_calculate_bearish_retracement(self):
        result = calculate_retracement_percent(
            120, 100, 112, "bearish"
        )
        self.assertAlmostEqual(result, 60.0)

    def test_invalid_impulse(self):
        with self.assertRaises(ValueError):
            calculate_retracement_percent(
                100, 100, 95, "bullish"
            )

    def test_pullback_outside_impulse(self):
        with self.assertRaises(ValueError):
            calculate_retracement_percent(
                100, 120, 95, "bullish"
            )

    # AUTOMATIC STRUCTURE LEVELS

    def test_confirmed_structure_levels(self):
        result = get_confirmed_structure_levels(
            self.data
        )

        self.assertTrue(result["levels_available"])
        self.assertEqual(result["swing_count"], 2)

        self.assertEqual(
            result["swing_high"]["price"], 16
        )

        self.assertEqual(
            result["swing_low"]["price"], 8
        )

    def test_invalid_structure_data(self):
        with self.assertRaises(ValueError):
            get_confirmed_structure_levels(
                self.data.drop(columns=["high"])
            )

    # BULLISH BOS

    def test_bullish_bos(self):
        self.assertTrue(
            confirm_bos("bullish", 105, 100)
        )

    def test_bullish_wick_only_break_not_confirmed(self):
        self.assertFalse(
            confirm_bos("bullish", 99, 100)
        )

    # BEARISH BOS

    def test_bearish_bos(self):
        self.assertTrue(
            confirm_bos("bearish", 95, 100)
        )

    def test_bearish_wick_only_break_not_confirmed(self):
        self.assertFalse(
            confirm_bos("bearish", 101, 100)
        )

    # CHOCH

    def test_bearish_choch_from_bullish_structure(self):
        self.assertTrue(
            confirm_choch("bullish", 95, 100)
        )

    def test_bullish_choch_from_bearish_structure(self):
        self.assertTrue(
            confirm_choch("bearish", 105, 100)
        )

    def test_no_choch_without_protected_swing(self):
        self.assertFalse(
            confirm_choch("bullish", 95, None)
        )

    # STRUCTURE EVENTS

    def test_bullish_structure_bos(self):
        result = evaluate_structure_event(
            direction="bullish",
            candle_close=110,
            swing_high=105,
            swing_low=90,
            protected_swing=95,
        )
        self.assertEqual(result, "BOS")

    def test_bullish_structure_choch(self):
        result = evaluate_structure_event(
            direction="bullish",
            candle_close=90,
            swing_high=105,
            swing_low=85,
            protected_swing=95,
        )
        self.assertEqual(result, "CHoCH")

    def test_no_structure_event(self):
        result = evaluate_structure_event(
            direction="bullish",
            candle_close=100,
            swing_high=105,
            swing_low=90,
            protected_swing=95,
        )
        self.assertEqual(result, "NONE")


if __name__ == "__main__":
    unittest.main()
