
import unittest
from unittest.mock import Mock, patch

import pandas as pd

from engines.market_data import fetch_ohlc


class TestMarketData(unittest.TestCase):

    def test_missing_api_key(self):
        with self.assertRaises(ValueError):
            fetch_ohlc(
                api_key="",
                symbol="XAU/USD",
            )

    def test_unsupported_symbol(self):
        with self.assertRaises(ValueError):
            fetch_ohlc(
                api_key="test_key",
                symbol="INVALID/USD",
            )

    def test_unsupported_interval(self):
        with self.assertRaises(ValueError):
            fetch_ohlc(
                api_key="test_key",
                symbol="XAU/USD",
                interval="2days",
            )

    def test_invalid_outputsize(self):
        with self.assertRaises(ValueError):
            fetch_ohlc(
                api_key="test_key",
                symbol="XAU/USD",
                outputsize=0,
            )

    @patch("engines.market_data.requests.get")
    def test_successful_market_data_fetch(self, mock_get):

        mock_response = Mock()

        mock_response.json.return_value = {
            "meta": {
                "symbol": "XAU/USD",
                "interval": "15min",
            },
            "values": [
                {
                    "datetime": "2026-11-27 10:15:00",
                    "open": "3642.0",
                    "high": "3645.0",
                    "low": "3640.0",
                    "close": "3643.0",
                },
                {
                    "datetime": "2026-11-27 10:00:00",
                    "open": "3640.0",
                    "high": "3644.0",
                    "low": "3638.0",
                    "close": "3642.0",
                },
            ],
            "status": "ok",
        }

        mock_get.return_value = mock_response

        result = fetch_ohlc(
            api_key="test_key",
            symbol="XAU/USD",
            interval="15min",
            outputsize=200,
        )

        self.assertIsInstance(result, pd.DataFrame)

        self.assertEqual(
            len(result),
            2,
        )

        self.assertTrue(
            pd.api.types.is_numeric_dtype(result["close"])
        )

        self.assertTrue(
            result["datetime"].is_monotonic_increasing
        )

        self.assertEqual(
            float(result.iloc[-1]["close"]),
            3643.0,
        )

        mock_get.assert_called_once()

    @patch("engines.market_data.requests.get")
    def test_provider_api_error(self, mock_get):

        mock_response = Mock()

        mock_response.json.return_value = {
            "status": "error",
            "message": "Invalid API key",
            "code": 401,
        }

        mock_get.return_value = mock_response

        with self.assertRaises(Exception):
            fetch_ohlc(
                api_key="invalid_key",
                symbol="XAU/USD",
            )


if __name__ == "__main__":
    unittest.main()
