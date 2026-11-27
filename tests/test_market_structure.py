
# ==========================================
# BIGMAN — MARKET STRUCTURE TESTS
# Tests for SMC-002
# ==========================================

import unittest

from engines.market_structure import (
    is_valid_pullback,
    confirm_bos,
    confirm_choch,
    evaluate_structure_event
)


class TestMarketStructure(unittest.TestCase):

    # --------------------------------------
    # PULLBACK VALIDATION
    # --------------------------------------

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

    # --------------------------------------
    # BULLISH BOS
    # --------------------------------------

    def test_bullish_bos(self):
        self.assertTrue(
            confirm_bos("bullish", 105, 100)
        )

    def test_bullish_wick_only_break_not_confirmed(self):
        # Candle close remains below swing high.
        self.assertFalse(
            confirm_bos("bullish", 99, 100)
        )

    # --------------------------------------
    # BEARISH BOS
    # --------------------------------------

    def test_bearish_bos(self):
        self.assertTrue(
            confirm_bos("bearish", 95, 100)
        )

    def test_bearish_wick_only_break_not_confirmed(self):
        # Candle close remains above swing low.
        self.assertFalse(
            confirm_bos("bearish", 101, 100)
        )

    # --------------------------------------
    # CHOCH
    # --------------------------------------

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

    # --------------------------------------
    # STRUCTURE EVENT
    # --------------------------------------

    def test_bullish_structure_bos(self):
        result = evaluate_structure_event(
            direction="bullish",
            candle_close=110,
            swing_high=105,
            swing_low=90,
            protected_swing=95
        )

        self.assertEqual(result, "BOS")

    def test_bullish_structure_choch(self):
        result = evaluate_structure_event(
            direction="bullish",
            candle_close=90,
            swing_high=105,
            swing_low=85,
            protected_swing=95
        )

        self.assertEqual(result, "CHoCH")

    def test_no_structure_event(self):
        result = evaluate_structure_event(
            direction="bullish",
            candle_close=100,
            swing_high=105,
            swing_low=90,
            protected_swing=95
        )

        self.assertEqual(result, "NONE")


if __name__ == "__main__":
    unittest.main()
