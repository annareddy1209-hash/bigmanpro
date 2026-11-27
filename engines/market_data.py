
# ==========================================
# BIGMAN — MARKET DATA ENGINE
# Provider: Twelve Data
# ==========================================

import requests
import pandas as pd


API_URL = "https://api.twelvedata.com/time_series"

SUPPORTED_SYMBOLS = {
    "Gold": "XAU/USD",
    "Bitcoin": "BTC/USD",
    "Ethereum": "ETH/USD"
}

SUPPORTED_INTERVALS = [
    "5min",
    "15min",
    "1h",
    "4h"
]


def fetch_ohlc(
    api_key,
    symbol,
    interval="15min",
    outputsize=200
):
    """
    Fetch OHLC market candles from Twelve Data.

    Returns:
        pandas DataFrame on success.
        Raises ValueError on provider/API errors.
    """

    if not api_key:
        raise ValueError("Twelve Data API key is missing.")

    if symbol not in SUPPORTED_SYMBOLS.values():
        raise ValueError("Unsupported market symbol.")

    if interval not in SUPPORTED_INTERVALS:
        raise ValueError("Unsupported timeframe.")

    if not 1 <= outputsize <= 5000:
        raise ValueError("Output size must be between 1 and 5000.")

    params = {
        "symbol": symbol,
        "interval": interval,
        "outputsize": outputsize,
        "timezone": "UTC",
        "apikey": api_key
    }

    try:
        response = requests.get(
            API_URL,
            params=params,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

    except requests.RequestException as error:
        raise ValueError(
            f"Market data connection failed: {error}"
        ) from error

    if data.get("status") == "error":
        raise ValueError(
            data.get("message", "Twelve Data API error.")
        )

    values = data.get("values")

    if not values:
        raise ValueError(
            "No candle data returned by provider."
        )

    df = pd.DataFrame(values)

    required_columns = [
        "datetime",
        "open",
        "high",
        "low",
        "close"
    ]

    missing = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing market data columns: {missing}"
        )

    df["datetime"] = pd.to_datetime(
        df["datetime"],
        errors="coerce",
        utc=True
    )

    for column in ["open", "high", "low", "close"]:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    df = df.dropna(
        subset=required_columns
    )

    df = df.sort_values(
        "datetime"
    ).reset_index(drop=True)

    if df.empty:
        raise ValueError("No valid OHLC candles available.")

    return df


def get_available_markets():
    return SUPPORTED_SYMBOLS.copy()


def get_available_timeframes():
    return SUPPORTED_INTERVALS.copy()
