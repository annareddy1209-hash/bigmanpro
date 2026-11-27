
import unittest
import pandas as pd

from engines.fvg import (
    identify_fvg,
    scan_fvgs,
    validate_candles,
)


class TestFVGEngine(unittest.TestCase):

    def bullish_data(self):
        return pd.DataFrame({
            "open":  [100, 104, 105, 103],
            "high":  [102, 108, 110, 106],
            "low":   [99, 103, 104, 101],
            "close": [101, 107, 109, 102],
        })

    def bearish_data(self):
        return pd.DataFrame({
            "open":  [108, 103, 100, 102],
            "high":  [110, 104, 102, 105],
            "low":   [106, 99, 98, 101],
            "close": [107, 100, 99, 104],
        })

    def test_bullish_fvg_detected(self):
        result = identify_fvg(
            self.bullish_data(),
            index=2,
            direction="BULLISH",
        )

        self.assertTrue(result["detected"])
        self.assertEqual(result["direction"], "BULLISH")
        self.assertEqual(result["zone_low"], 102.0)
        self.assertEqual(result["zone_high"], 104.0)
        self.assertEqual(result["midpoint"], 103.0)

    def test_bearish_fvg_detected(self):
        result = identify_fvg(
            self.bearish_data(),
            index=2,
            direction="BEARISH",
        )

        self.assertTrue(result["detected"])
        self.assertEqual(result["direction"], "BEARISH")
        self.assertEqual(result["zone_low"], 102.0)
        self.assertEqual(result["zone_high"], 106.0)

    def test_no_bullish_gap(self):
        data = pd.DataFrame({
            "open": [100, 101, 102],
            "high": [103, 104, 105],
            "low": [99, 100, 101],
            "close": [102, 103, 104],
        })

        result = identify_fvg(
            data,
            index=2,
            direction="BULLISH",
        )

        self.assertFalse(result["detected"])

    def test_full_mitigation(self):
        result = identify_fvg(
            self.bullish_data(),
            index=2,
            direction="BULLISH",
            require_unmitigated=True,
            mitigation_mode="full",
        )

        self.assertFalse(result["detected"])
        self.assertTrue(result["mitigated"])

    def test_mitigated_fvg_can_be_returned(self):
        result = identify_fvg(
            self.bullish_data(),
            index=2,
            direction="BULLISH",
            require_unmitigated=False,
        )

        self.assertTrue(result["detected"])
        self.assertTrue(result["mitigated"])

    def test_invalid_direction(self):
        with self.assertRaises(ValueError):
            identify_fvg(
                self.bullish_data(),
                index=2,
                direction="SIDEWAYS",
            )

    def test_invalid_index(self):
        with self.assertRaises(ValueError):
            identify_fvg(
                self.bullish_data(),
                index=1,
                direction="BULLISH",
            )

    def test_invalid_mitigation_mode(self):
        with self.assertRaises(ValueError):
            identify_fvg(
                self.bullish_data(),
                index=2,
                direction="BULLISH",
                mitigation_mode="wrong",
            )

    def test_scan_fvgs(self):
        results = scan_fvgs(
            self.bullish_data(),
            direction="BULLISH",
            require_unmitigated=False,
        )

        self.assertGreaterEqual(len(results), 1)

    def test_invalid_candle_data(self):
        data = pd.DataFrame({
            "open": [100],
            "high": [90],
            "low": [95],
            "close": [102],
        })

        with self.assertRaises(ValueError):
            validate_candles(data)


if __name__ == "__main__":
    unittest.main()
