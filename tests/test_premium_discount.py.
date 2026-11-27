
import unittest

from engines.premium_discount import calculate_premium_discount


class TestPremiumDiscount(unittest.TestCase):

    def test_bullish_discount(self):
        result = calculate_premium_discount(
            current_price=40,
            dealing_range_high=100,
            dealing_range_low=0,
            direction="BULLISH",
        )

        self.assertEqual(result["location"], "DISCOUNT")
        self.assertTrue(result["favorable_location"])
        self.assertEqual(result["equilibrium"], 50)

    def test_bearish_premium(self):
        result = calculate_premium_discount(
            current_price=80,
            dealing_range_high=100,
            dealing_range_low=0,
            direction="BEARISH",
        )

        self.assertEqual(result["location"], "PREMIUM")
        self.assertTrue(result["favorable_location"])

    def test_equilibrium(self):
        result = calculate_premium_discount(
            current_price=50,
            dealing_range_high=100,
            dealing_range_low=0,
        )

        self.assertEqual(result["location"], "EQUILIBRIUM")
        self.assertEqual(result["position_percent"], 50)

    def test_bullish_premium_is_not_favorable(self):
        result = calculate_premium_discount(
            current_price=75,
            dealing_range_high=100,
            dealing_range_low=0,
            direction="BULLISH",
        )

        self.assertEqual(result["location"], "PREMIUM")
        self.assertFalse(result["favorable_location"])

    def test_bearish_discount_is_not_favorable(self):
        result = calculate_premium_discount(
            current_price=25,
            dealing_range_high=100,
            dealing_range_low=0,
            direction="BEARISH",
        )

        self.assertEqual(result["location"], "DISCOUNT")
        self.assertFalse(result["favorable_location"])

    def test_invalid_range(self):
        with self.assertRaises(ValueError):
            calculate_premium_discount(
                current_price=50,
                dealing_range_high=20,
                dealing_range_low=20,
            )

    def test_price_outside_range(self):
        with self.assertRaises(ValueError):
            calculate_premium_discount(
                current_price=110,
                dealing_range_high=100,
                dealing_range_low=0,
            )

    def test_invalid_direction(self):
        with self.assertRaises(ValueError):
            calculate_premium_discount(
                current_price=50,
                dealing_range_high=100,
                dealing_range_low=0,
                direction="SIDEWAYS",
            )

    def test_invalid_price(self):
        with self.assertRaises(ValueError):
            calculate_premium_discount(
                current_price=float("nan"),
                dealing_range_high=100,
                dealing_range_low=0,
            )


if __name__ == "__main__":
    unittest.main()
