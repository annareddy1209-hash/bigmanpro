
import pandas as pd


REQUIRED_COLUMNS = [
    "datetime",
    "open",
    "high",
    "low",
    "close",
]


def validate_ohlc(data):
    """Validate and prepare OHLC candle data."""

    if not isinstance(data, pd.DataFrame):
        raise TypeError("Market data must be a pandas DataFrame.")

    missing = [
        column for column in REQUIRED_COLUMNS
        if column not in data.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {', '.join(missing)}"
        )

    if data.empty:
        raise ValueError("Market data is empty.")

    candles = data.copy()

    for column in ["high", "low", "open", "close"]:
        candles[column] = pd.to_numeric(
            candles[column], errors="coerce"
        )

    if candles[["high", "low", "open", "close"]].isna().any().any():
        raise ValueError("Invalid OHLC values detected.")

    if (
        (candles["high"] < candles["low"]).any()
        or (candles["high"] < candles["open"]).any()
        or (candles["high"] < candles["close"]).any()
        or (candles["low"] > candles["open"]).any()
        or (candles["low"] > candles["close"]).any()
    ):
        raise ValueError("Invalid candle structure detected.")

    return candles.reset_index(drop=True)


def detect_swing_points(
    data: pd.DataFrame,
    left_bars: int = 2,
    right_bars: int = 2,
):
    """
    Detect confirmed swing highs and swing lows.

    A swing is confirmed only after the required
    number of candles on its right have closed.

    Equal highs/lows are not treated as unique pivots.

    The final unconfirmed candles are excluded.
    """

    if not isinstance(left_bars, int) or left_bars < 1:
        raise ValueError("left_bars must be a positive integer.")

    if not isinstance(right_bars, int) or right_bars < 1:
        raise ValueError("right_bars must be a positive integer.")

    candles = validate_ohlc(data)

    swings = []

    for index in range(
        left_bars,
        len(candles) - right_bars
    ):
        current_high = candles.iloc[index]["high"]
        current_low = candles.iloc[index]["low"]

        left = candles.iloc[index-left_bars:index]
        right = candles.iloc[index+1:index+right_bars+1]

        is_swing_high = (
            current_high > left["high"].max()
            and current_high > right["high"].max()
        )

        is_swing_low = (
            current_low < left["low"].min()
            and current_low < right["low"].min()
        )

        if is_swing_high:
            swings.append({
                "index": index,
                "datetime": candles.iloc[index]["datetime"],
                "price": float(current_high),
                "type": "swing_high",
                "confirmation_index": index + right_bars,
            })

        if is_swing_low:
            swings.append({
                "index": index,
                "datetime": candles.iloc[index]["datetime"],
                "price": float(current_low),
                "type": "swing_low",
                "confirmation_index": index + right_bars,
            })

    return sorted(
        swings,
        key=lambda item: item["index"]
    )


def get_latest_swings(data, left_bars=2, right_bars=2):
    """Return the latest confirmed swing high and low."""

    swings = detect_swing_points(
        data,
        left_bars=left_bars,
        right_bars=right_bars,
    )

    latest_high = next(
        (
            swing for swing in reversed(swings)
            if swing["type"] == "swing_high"
        ),
        None,
    )

    latest_low = next(
        (
            swing for swing in reversed(swings)
            if swing["type"] == "swing_low"
        ),
        None,
    )

    return {
        "latest_swing_high": latest_high,
        "latest_swing_low": latest_low,
        "total_swings": len(swings),
    }
