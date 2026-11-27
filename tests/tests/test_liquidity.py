
import unittest
import pandas as pd

from engines.liquidity import (
    detect_liquidity_sweep,
    scan_liquidity_sweeps,
    validate_candles,
)


class TestLiquidityEngine(unittest.TestCase):

    def test_sell_side_bullish_sweep(self):
        data = pd.DataFrame({
            "open": [105],
            "high": [108],
            "low": [98],
            "close": [103],
        })

        result = detect_liquidity_sweep(
            data,
            liquidity_level=100,
            liquidity_side="sell_side",
        )

        self.assertTrue(result["detected"])
        self.assertEqual(result["direction"], "BULLISH")
        self.assertEqual(result["sweep_distance"], 2)

    def test_buy_side_bearish_sweep(self):
        data = pd.DataFrame({
            "open": [105],
            "high": [112],
            "low": [102],
            "close": [108],
        })

        result = detect_liquidity_sweep(
            data,
            liquidity_level=110,
            liquidity_side="buy_side",
        )

        self.assertTrue(result["detected"])
        self.assertEqual(result["direction"], "BEARISH")
        self.assertEqual(result["sweep_distance"], 2)

    def test_no_sweep_when_price_does_not_cross_level(self):
        data = pd.DataFrame({
            "open": [105],
            "high": [109],
            "low": [101],
            "close": [106],
        })

        result = detect_liquidity_sweep(
            data,
            liquidity_level=100,
            liquidity_side="sell_side",
        )

        self.assertFalse(result["detected"])
        self.assertEqual(result["direction"], "NONE")

    def test_cross_without_reclaim_is_not_sweep(self):
        data = pd.DataFrame({
            "open": [101],
            "high": [103],
            "low": [98],
            "close": [99],
        })

        result = detect_liquidity_sweep(
            data,
            liquidity_level=100,
            liquidity_side="sell_side",
        )

        self.assertFalse(result["detected"])

    def test_invalid_liquidity_side(self):
        data = pd.DataFrame({
            "open": [105],
            "high": [108],
            "low": [98],
            "close": [103],
        })

        with self.assertRaises(ValueError):
            detect_liquidity_sweep(
                data,
                100,
                "invalid_side",
            )

    def test_invalid_candles(self):
        data = pd.DataFrame({
            "open": [105],
            "high": [95],
            "low": [98],
            "close": [103],
        })

        with self.assertRaises(ValueError):
            validate_candles(data)

    def test_scan_multiple_candles(self):
        data = pd.DataFrame({
            "open": [105, 104, 102],
            "high": [108, 107, 106],
            "low": [101, 98, 97],
            "close": [104, 103, 102],
        })

        events = scan_liquidity_sweeps(
            data,
            liquidity_level=100,
            liquidity_side="sell_side",
        )

        self.assertEqual(len(events), 2)
        self.assertEqual(events[0]["candle_index"], 1)
        self.assertEqual(events[1]["candle_index"], 2)


if __name__ == "__main__":
    unittest.main()
