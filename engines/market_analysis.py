
from engines.market_data import fetch_ohlc
from engines.charts import create_candlestick_chart


def analyze_market(
    api_key: str,
    symbol: str,
    interval: str = "15min",
    outputsize: int = 200,
):
    """
    Fetch market candles and create a candlestick chart.

    This function performs market analysis preparation only.
    It does not place trades.
    """

    if not api_key:
        raise ValueError("Twelve Data API key is missing.")

    market_data = fetch_ohlc(
        api_key=api_key,
        symbol=symbol,
        interval=interval,
        outputsize=outputsize,
    )

    if market_data is None or market_data.empty:
        raise ValueError(
            f"No market data returned for {symbol}."
        )

    chart = create_candlestick_chart(
        data=market_data,
        symbol=symbol,
        interval=interval,
    )

    latest_price = float(
        market_data.iloc[-1]["close"]
    )

    previous_price = (
        float(market_data.iloc[-2]["close"])
        if len(market_data) > 1
        else latest_price
    )

    change = latest_price - previous_price

    change_percent = (
        (change / previous_price) * 100
        if previous_price != 0
        else 0.0
    )

    return {
        "symbol": symbol,
        "interval": interval,
        "data": market_data,
        "chart": chart,
        "latest_price": latest_price,
        "previous_price": previous_price,
        "change": change,
        "change_percent": change_percent,
        "candles_count": len(market_data),
    }
