
import unittest
import pandas as pd
import plotly.graph_objects as go

from engines.charts import create_candlestick_chart


class TestCandlestickChart(unittest.TestCase):

    def setUp(self):
        self.data = pd.DataFrame({
            "datetime": [
                "2026-11-27 10:00:00",
                "2026-11-27 10:15:00",
            ],
            "open": [100, 105],
            "high": [110, 112],
            "low": [98, 103],
            "close": [108, 107],
        })

    def test_chart_creation(self):
        chart = create_candlestick_chart(
            self.data,
            symbol="BTC/USD",
            interval="15min",
        )

        self.assertIsInstance(chart, go.Figure)
        self.assertEqual(len(chart.data), 1)
        self.assertEqual(chart.data[0].type, "candlestick")

    def test_empty_data_rejected(self):
        with self.assertRaises(ValueError):
            create_candlestick_chart(
                pd.DataFrame(),
            )

    def test_missing_columns_rejected(self):
        invalid_data = pd.DataFrame({
            "datetime": ["2026-11-27 10:00:00"],
            "open": [100],
        })

        with self.assertRaises(ValueError):
            create_candlestick_chart(invalid_data)

    def test_invalid_ohlc_rejected(self):
        invalid_data = pd.DataFrame({
            "datetime": ["2026-11-27 10:00:00"],
            "open": [100],
            "high": [90],
            "low": [95],
            "close": [105],
        })

        with self.assertRaises(ValueError):
            create_candlestick_chart(invalid_data)


if __name__ == "__main__":
    unittest.main()
