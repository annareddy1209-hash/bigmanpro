
import unittest

from engines.risk_management import calculate_position_risk


class TestRiskManagement(unittest.TestCase):

    def test_buy_position_calculation(self):
        result = calculate_position_risk(
            account_balance=1000,
            risk_percent=1,
            entry_price=100,
            stop_loss=98,
            direction="BUY",
            point_value_per_unit=1,
        )

        self.assertEqual(result["risk_amount"], 10)
        self.assertEqual(result["stop_distance"], 2)
        self.assertEqual(result["position_size_units"], 5)
        self.assertEqual(result["targets"]["TP_2R"], 104)
        self.assertEqual(result["targets"]["TP_3R"], 106)

    def test_sell_position_calculation(self):
        result = calculate_position_risk(
            account_balance=1000,
            risk_percent=1,
            entry_price=100,
            stop_loss=102,
            direction="SELL",
            point_value_per_unit=1,
        )

        self.assertEqual(result["position_size_units"], 5)
        self.assertEqual(result["targets"]["TP_2R"], 96)
        self.assertEqual(result["targets"]["TP_3R"], 94)

    def test_risk_amount(self):
        result = calculate_position_risk(
            account_balance=5000,
            risk_percent=2,
            entry_price=100,
            stop_loss=95,
            direction="BUY",
        )

        self.assertEqual(result["risk_amount"], 100)

    def test_risk_above_limit_rejected(self):
        with self.assertRaises(ValueError):
            calculate_position_risk(
                account_balance=1000,
                risk_percent=3,
                entry_price=100,
                stop_loss=98,
                direction="BUY",
            )

    def test_buy_invalid_stop_loss(self):
        with self.assertRaises(ValueError):
            calculate_position_risk(
                account_balance=1000,
                risk_percent=1,
                entry_price=100,
                stop_loss=101,
                direction="BUY",
            )

    def test_sell_invalid_stop_loss(self):
        with self.assertRaises(ValueError):
            calculate_position_risk(
                account_balance=1000,
                risk_percent=1,
                entry_price=100,
                stop_loss=99,
                direction="SELL",
            )

    def test_invalid_direction(self):
        with self.assertRaises(ValueError):
            calculate_position_risk(
                account_balance=1000,
                risk_percent=1,
                entry_price=100,
                stop_loss=98,
                direction="HOLD",
            )

    def test_invalid_balance(self):
        with self.assertRaises(ValueError):
            calculate_position_risk(
                account_balance=0,
                risk_percent=1,
                entry_price=100,
                stop_loss=98,
                direction="BUY",
            )

    def test_invalid_reward_ratio(self):
        with self.assertRaises(ValueError):
            calculate_position_risk(
                account_balance=1000,
                risk_percent=1,
                entry_price=100,
                stop_loss=98,
                direction="BUY",
                reward_ratios=(2, 0),
            )

    def test_invalid_point_value(self):
        with self.assertRaises(ValueError):
            calculate_position_risk(
                account_balance=1000,
                risk_percent=1,
                entry_price=100,
                stop_loss=98,
                direction="BUY",
                point_value_per_unit=0,
            )

    def test_live_trading_disabled(self):
        result = calculate_position_risk(
            account_balance=1000,
            risk_percent=1,
            entry_price=100,
            stop_loss=98,
            direction="BUY",
        )

        self.assertFalse(result["live_trading"])


if __name__ == "__main__":
    unittest.main()
