
# ==========================================
# BIGMAN — MARKET DATA ENGINE TESTS
# ==========================================

import unittest
from unittest.mock import patch, Mock

from engines.market_data import fetch_ohlc


class TestMarketData(unittest.TestCase):

    def test_missing_api_key(self):
        with self.assertRaises(ValueError):
            fetch_ohlc("", "XAU/USD")

    def test_unsupported_symbol(self):
        with self.assertRaises(ValueError):
            fetch_ohlc("test_key", "INVALID/USD")

    def test_unsupported_timeframe(self):
        with self.assertRaises(ValueError):
            fetch_ohlc("test_key", "BTC/USD", "1day")

    def test_invalid_outputsize(self):
        with self.assertRaises(ValueError):
            fetch_ohlc(
                "test_key",
                "BTC/USD",
                outputsize=6000
            )

    @patch("engines.market_data.requests.get")
    def test_successful_market_data(self, mock_get):

        response = Mock()

        response.json.return_value = {
            "meta": {
                "symbol": "BTC/USD",
                "interval": "15min"
            },
            "values": [
                {
                    "datetime": "2026-11-27 10:15:00",
                    "open": "90000",
                    "high": "90500",
                    "low": "89900",
                    "close": "90300"
                },
                {
                    "datetime": "2026-11-27 10:00:00",
                    "open": "89800",
                    "high": "90200",
                    "low": "89700",
                    "close": "90000"
                }
            ]
        }

        mock_get.return_value = response

        df = fetch_ohlc(
            "test_key",
            "BTC/USD",
            "15min"
        )

        self.assertEqual(len(df), 2)
        self.assertEqual(
            list(df.columns[:5]),
            ["datetime", "open", "high", "low", "close"]
        )

        self.assertTrue(
            df["datetime"].is_monotonic_increasing
        )

    @patch("engines.market_data.requests.get")
    def test_provider_error(self, mock_get):

        response = Mock()

        response.json.return_value = {
            "status": "error",
            "message": "Invalid API key"
        }

        mock_get.return_value = response

        with self.assertRaises(ValueError):
            fetch_ohlc(
                "wrong_key",
                "BTC/USD"
            )


if __name__ == "__main__":
    unittest.main()
