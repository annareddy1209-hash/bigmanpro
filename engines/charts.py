
import pandas as pd
import plotly.graph_objects as go


REQUIRED_COLUMNS = [
    "datetime",
    "open",
    "high",
    "low",
    "close",
]


def create_candlestick_chart(
    data: pd.DataFrame,
    symbol: str = "Market",
    interval: str = "15min",
):
    """
    Create an interactive candlestick chart.

    Expected columns:
    datetime, open, high, low, close
    """

    if not isinstance(data, pd.DataFrame):
        raise TypeError("Market data must be a pandas DataFrame.")

    missing = [
        column
        for column in REQUIRED_COLUMNS
        if column not in data.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {', '.join(missing)}"
        )

    if data.empty:
        raise ValueError("No market data available to display.")

    chart_data = data.copy()

    chart_data["datetime"] = pd.to_datetime(
        chart_data["datetime"],
        errors="coerce",
        utc=True,
    )

    for column in ["open", "high", "low", "close"]:
        chart_data[column] = pd.to_numeric(
            chart_data[column],
            errors="coerce",
        )

    chart_data = chart_data.dropna(
        subset=REQUIRED_COLUMNS
    )

    if chart_data.empty:
        raise ValueError("No valid candles found in market data.")

    chart_data = chart_data.sort_values(
        "datetime"
    ).reset_index(drop=True)

    if (
        (chart_data["high"] < chart_data["low"]).any()
        or (chart_data["high"] < chart_data["open"]).any()
        or (chart_data["high"] < chart_data["close"]).any()
        or (chart_data["low"] > chart_data["open"]).any()
        or (chart_data["low"] > chart_data["close"]).any()
    ):
        raise ValueError("Invalid OHLC candle values detected.")

    figure = go.Figure()

    figure.add_trace(
        go.Candlestick(
            x=chart_data["datetime"],
            open=chart_data["open"],
            high=chart_data["high"],
            low=chart_data["low"],
            close=chart_data["close"],
            name=symbol,
            increasing_line_color="#20d9c4",
            decreasing_line_color="#ff5c70",
        )
    )

    figure.update_layout(
        title=f"{symbol} — {interval} Candlestick Chart",
        template="plotly_dark",
        height=550,
        xaxis_title="Time (UTC)",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False,
        hovermode="x unified",
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20,
        ),
    )

    return figure
