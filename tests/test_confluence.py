
import unittest

from engines.confluence import evaluate_confluence


class TestConfluenceEngine(unittest.TestCase):

    def test_bullish_confluence_passes(self):
        result = evaluate_confluence(
            direction="BULLISH",
            confirmations={
                "mtf_alignment": True,
                "market_structure": True,
                "liquidity_sweep": True,
                "fvg": False,
            },
            minimum_confirmations=3,
        )

        self.assertTrue(result["eligible"])
        self.assertEqual(result["score"], 3)
        self.assertEqual(result["status"], "CONFIRMED")

    def test_bearish_confluence_passes(self):
        result = evaluate_confluence(
            direction="BEARISH",
            confirmations={
                "mtf_alignment": "BEARISH",
                "market_structure": "BEARISH",
                "liquidity_sweep": True,
            },
            minimum_confirmations=3,
        )

        self.assertTrue(result["eligible"])
        self.assertEqual(result["direction"], "BEARISH")

    def test_insufficient_confirmations(self):
        result = evaluate_confluence(
            direction="BULLISH",
            confirmations={
                "mtf_alignment": True,
                "market_structure": False,
                "fvg": False,
            },
            minimum_confirmations=2,
        )

        self.assertFalse(result["eligible"])
        self.assertEqual(result["status"], "WAIT")

    def test_required_confirmation_missing(self):
        with self.assertRaises(ValueError):
            evaluate_confluence(
                direction="BULLISH",
                confirmations={
                    "mtf_alignment": True,
                    "fvg": True,
                },
                required_confirmations=[
                    "market_structure"
                ],
            )

    def test_required_confirmation_fails(self):
        result = evaluate_confluence(
            direction="BULLISH",
            confirmations={
                "mtf_alignment": True,
                "market_structure": False,
                "fvg": True,
            },
            required_confirmations=[
                "market_structure"
            ],
            minimum_confirmations=2,
        )

        self.assertFalse(result["eligible"])
        self.assertIn(
            "market_structure",
            result["required_failed"],
        )

    def test_directional_conflict(self):
        result = evaluate_confluence(
            direction="BULLISH",
            confirmations={
                "mtf_alignment": "BEARISH",
                "market_structure": "BULLISH",
                "fvg": "NEUTRAL",
            },
            minimum_confirmations=2,
        )

        self.assertFalse(result["eligible"])
        self.assertEqual(result["score"], 1)

    def test_invalid_direction(self):
        with self.assertRaises(ValueError):
            evaluate_confluence(
                direction="SIDEWAYS",
                confirmations={"fvg": True},
            )

    def test_empty_confirmations(self):
        with self.assertRaises(ValueError):
            evaluate_confluence(
                direction="BULLISH",
                confirmations={},
            )

    def test_invalid_confirmation_value(self):
        with self.assertRaises(ValueError):
            evaluate_confluence(
                direction="BULLISH",
                confirmations={
                    "fvg": "MAYBE"
                },
            )

    def test_invalid_minimum(self):
        with self.assertRaises(ValueError):
            evaluate_confluence(
                direction="BULLISH",
                confirmations={"fvg": True},
                minimum_confirmations=0,
            )

    def test_invalid_minimum_type(self):
        with self.assertRaises(ValueError):
            evaluate_confluence(
                direction="BULLISH",
                confirmations={"fvg": True},
                minimum_confirmations=1.5,
            )

    def test_minimum_exceeds_available(self):
        with self.assertRaises(ValueError):
            evaluate_confluence(
                direction="BULLISH",
                confirmations={"fvg": True},
                minimum_confirmations=2,
            )


if __name__ == "__main__":
    unittest.main()
