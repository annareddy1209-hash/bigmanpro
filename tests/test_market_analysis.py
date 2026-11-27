
import unittest
from unittest.mock import patch

import pandas as pd
import plotly.graph_objects as go

from engines.market_analysis import analyze_market


class TestMarketAnalysis(unittest.TestCase):

    def setUp(self):
        self.sample_data = pd.DataFrame({
            "datetime": [
                "2026-11-27 10:00:00",
                "2026-11-27 10:15:00",
            ],
            "open": [100, 105],
            "high": [110, 112],
            "low": [98, 103],
            "close": [108, 107],
        })

    @patch("engines.market_analysis.fetch_ohlc")
    def test_successful_analysis(self, mock_fetch):
        mock_fetch.return_value = self.sample_data

        result = analyze_market(
            api_key="test_key",
            symbol="BTC/USD",
            interval="15min",
        )

        self.assertEqual(result["symbol"], "BTC/USD")
        self.assertEqual(result["candles_count"], 2)
        self.assertEqual(result["latest_price"], 107.0)
        self.assertEqual(result["previous_price"], 108.0)
        self.assertIsInstance(result["chart"], go.Figure)

        mock_fetch.assert_called_once()

    def test_missing_api_key(self):
        with self.assertRaises(ValueError):
            analyze_market(
                api_key="",
                symbol="BTC/USD",
            )

    @patch("engines.market_analysis.fetch_ohlc")
    def test_empty_market_data(self, mock_fetch):
        mock_fetch.return_value = pd.DataFrame()

        with self.assertRaises(ValueError):
            analyze_market(
                api_key="test_key",
                symbol="BTC/USD",
            )

    @patch("engines.market_analysis.fetch_ohlc")
    def test_api_error_propagates(self, mock_fetch):
        mock_fetch.side_effect = RuntimeError(
            "Market provider unavailable"
        )

        with self.assertRaises(RuntimeError):
            analyze_market(
                api_key="test_key",
                symbol="BTC/USD",
            )


if __name__ == "__main__":
    unittest.main()
