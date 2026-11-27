
import unittest
import pandas as pd

from engines.order_blocks import (
    identify_order_block,
    validate_candles,
)


class TestOrderBlockEngine(unittest.TestCase):

    def bullish_data(self):
        return pd.DataFrame({
            "open":  [100, 101, 101, 99],
            "high":  [102, 103, 102, 106],
            "low":   [98, 99, 97, 98],
            "close": [101, 102, 99, 105],
        })

    def bearish_data(self):
        return pd.DataFrame({
            "open":  [100, 99, 99, 101],
            "high":  [102, 101, 103, 102],
            "low":   [98, 97, 98, 94],
            "close": [99, 98, 101, 95],
        })

    def test_valid_bullish_order_block(self):
        result = identify_order_block(
            self.bullish_data(),
            bos_index=3,
            direction="BULLISH",
            bos_confirmed=True,
            fvg_confirmed=True,
        )

        self.assertTrue(result["detected"])
        self.assertEqual(result["direction"], "BULLISH")
        self.assertEqual(result["ob_index"], 2)
        self.assertEqual(result["zone_high"], 102.0)
        self.assertEqual(result["zone_low"], 97.0)

    def test_valid_bearish_order_block(self):
        result = identify_order_block(
            self.bearish_data(),
            bos_index=3,
            direction="BEARISH",
            bos_confirmed=True,
            fvg_confirmed=True,
        )

        self.assertTrue(result["detected"])
        self.assertEqual(result["direction"], "BEARISH")
        self.assertEqual(result["ob_index"], 2)

    def test_unconfirmed_bos_rejected(self):
        result = identify_order_block(
            self.bullish_data(),
            bos_index=3,
            direction="BULLISH",
            bos_confirmed=False,
            fvg_confirmed=True,
        )

        self.assertFalse(result["detected"])

    def test_missing_fvg_rejected(self):
        result = identify_order_block(
            self.bullish_data(),
            bos_index=3,
            direction="BULLISH",
            bos_confirmed=True,
            fvg_confirmed=False,
        )

        self.assertFalse(result["detected"])

    def test_fvg_requirement_can_be_disabled(self):
        result = identify_order_block(
            self.bullish_data(),
            bos_index=3,
            direction="BULLISH",
            bos_confirmed=True,
            fvg_confirmed=False,
            require_fvg=False,
        )

        self.assertTrue(result["detected"])

    def test_used_order_block_rejected(self):
        result = identify_order_block(
            self.bullish_data(),
            bos_index=3,
            direction="BULLISH",
            bos_confirmed=True,
            fvg_confirmed=True,
            already_used=True,
        )

        self.assertFalse(result["detected"])

    def test_wrong_bos_direction_rejected(self):
        result = identify_order_block(
            self.bullish_data(),
            bos_index=3,
            direction="BEARISH",
            bos_confirmed=True,
            fvg_confirmed=True,
        )

        self.assertFalse(result["detected"])

    def test_invalid_bos_index(self):
        with self.assertRaises(ValueError):
            identify_order_block(
                self.bullish_data(),
                bos_index=10,
                direction="BULLISH",
                bos_confirmed=True,
                fvg_confirmed=True,
            )

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
