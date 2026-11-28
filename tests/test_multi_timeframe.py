
import unittest
from unittest.mock import patch

from engines.multi_timeframe import (
    evaluate_mtf_alignment,
    normalize_bias,
    TIMEFRAME_PRESETS,
    analyze_multi_timeframe,
)


class TestMultiTimeframe(unittest.TestCase):

    def test_bullish_alignment(self):
        result = evaluate_mtf_alignment(
            htf_bias="BULLISH",
            mtf_bias="BULLISH",
            ltf_bias="BULLISH",
        )

        self.assertTrue(result["aligned"])
        self.assertEqual(result["direction"], "BULLISH")
        self.assertTrue(result["buy_allowed_by_alignment"])
        self.assertFalse(result["sell_allowed_by_alignment"])

    def test_bearish_alignment(self):
        result = evaluate_mtf_alignment(
            htf_bias="BEARISH",
            mtf_bias="BEARISH",
            ltf_bias="BEARISH",
        )

        self.assertTrue(result["aligned"])
        self.assertEqual(result["direction"], "BEARISH")
        self.assertTrue(result["sell_allowed_by_alignment"])
        self.assertFalse(result["buy_allowed_by_alignment"])

    def test_conflicting_timeframes(self):
        result = evaluate_mtf_alignment(
            htf_bias="BULLISH",
            mtf_bias="BEARISH",
            ltf_bias="BULLISH",
        )

        self.assertFalse(result["aligned"])
        self.assertEqual(result["direction"], "NEUTRAL")
        self.assertFalse(result["buy_allowed_by_alignment"])
        self.assertFalse(result["sell_allowed_by_alignment"])

    def test_neutral_timeframe_blocks_alignment(self):
        result = evaluate_mtf_alignment(
            htf_bias="BULLISH",
            mtf_bias="NEUTRAL",
            ltf_bias="BULLISH",
        )

        self.assertFalse(result["aligned"])
        self.assertEqual(result["status"], "NOT_ALIGNED")

    def test_intraday_timeframes(self):
        result = evaluate_mtf_alignment(
            "BULLISH",
            "BULLISH",
            "BULLISH",
            preset="INTRADAY",
        )

        self.assertEqual(
            result["timeframes"],
            {
                "HTF": "4h",
                "MTF": "1h",
                "LTF": "15min",
            },
        )

    def test_swing_timeframes(self):
        result = evaluate_mtf_alignment(
            "BEARISH",
            "BEARISH",
            "BEARISH",
            preset="SWING",
        )

        self.assertEqual(
            result["timeframes"]["HTF"],
            "4h",
        )

    def test_scalping_timeframes(self):
        result = evaluate_mtf_alignment(
            "BULLISH",
            "BULLISH",
            "BULLISH",
            preset="SCALPING",
        )

        self.assertEqual(
            result["timeframes"],
            {
                "HTF": "1h",
                "MTF": "15min",
                "LTF": "5min",
            },
        )

    def test_invalid_preset(self):
        with self.assertRaises(ValueError):
            evaluate_mtf_alignment(
                "BULLISH",
                "BULLISH",
                "BULLISH",
                preset="UNKNOWN",
            )

    def test_invalid_bias(self):
        with self.assertRaises(ValueError):
            evaluate_mtf_alignment(
                "BULLISH",
                "SIDEWAYS",
                "BULLISH",
            )

    def test_normalize_bias(self):
        self.assertEqual(
            normalize_bias(" bullish "),
            "BULLISH",
        )

    def test_invalid_bias_type(self):
        with self.assertRaises(ValueError):
            normalize_bias(None)

    def test_timeframe_presets_exist(self):
        self.assertIn("INTRADAY", TIMEFRAME_PRESETS)
        self.assertIn("SWING", TIMEFRAME_PRESETS)
        self.assertIn("SCALPING", TIMEFRAME_PRESETS)

    # ==========================================
    # AUTOMATIC MULTI-TIMEFRAME TESTS
    # ==========================================

    @patch("engines.market_bias.analyze_market_bias")
    def test_automatic_bullish_alignment(self, mock_analysis):

        mock_analysis.return_value = {
            "bias": "BULLISH",
            "status": "ANALYZED",
            "reason": "Higher highs and higher lows.",
        }

        market_data = {
            "4h": object(),
            "1h": object(),
            "15min": object(),
        }

        result = analyze_multi_timeframe(market_data)

        self.assertTrue(result["aligned"])
        self.assertEqual(result["direction"], "BULLISH")
        self.assertTrue(result["buy_allowed_by_alignment"])
        self.assertEqual(mock_analysis.call_count, 3)

    @patch("engines.market_bias.analyze_market_bias")
    def test_automatic_bearish_alignment(self, mock_analysis):

        mock_analysis.return_value = {
            "bias": "BEARISH",
            "status": "ANALYZED",
            "reason": "Lower highs and lower lows.",
        }

        market_data = {
            "4h": object(),
            "1h": object(),
            "15min": object(),
        }

        result = analyze_multi_timeframe(market_data)

        self.assertTrue(result["aligned"])
        self.assertEqual(result["direction"], "BEARISH")
        self.assertTrue(result["sell_allowed_by_alignment"])

    @patch("engines.market_bias.analyze_market_bias")
    def test_missing_timeframe_blocks_alignment(self, mock_analysis):

        mock_analysis.return_value = {
            "bias": "BULLISH",
            "status": "ANALYZED",
            "reason": "Bullish structure.",
        }

        market_data = {
            "4h": object(),
            "1h": object(),
            # 15min data intentionally missing
        }

        result = analyze_multi_timeframe(market_data)

        self.assertFalse(result["aligned"])
        self.assertEqual(result["direction"], "NEUTRAL")
        self.assertFalse(result["buy_allowed_by_alignment"])
        self.assertFalse(result["sell_allowed_by_alignment"])
        self.assertEqual(
            result["timeframe_analysis"]["LTF"]["status"],
            "MISSING_DATA",
        )

    def test_invalid_market_data_type(self):

        with self.assertRaises(ValueError):
            analyze_multi_timeframe(
                market_data_by_timeframe=None
            )

    def test_automatic_scalping_timeframes(self):

        with patch(
            "engines.market_bias.analyze_market_bias"
        ) as mock_analysis:

            mock_analysis.return_value = {
                "bias": "BULLISH",
                "status": "ANALYZED",
                "reason": "Bullish structure.",
            }

            market_data = {
                "1h": object(),
                "15min": object(),
                "5min": object(),
            }

            result = analyze_multi_timeframe(
                market_data,
                preset="SCALPING",
            )

            self.assertEqual(
                result["timeframe_analysis"]["HTF"]["timeframe"],
                "1h",
            )

            self.assertEqual(
                result["timeframe_analysis"]["LTF"]["timeframe"],
                "5min",
            )

            self.assertTrue(result["aligned"])


if __name__ == "__main__":
    unittest.main()
