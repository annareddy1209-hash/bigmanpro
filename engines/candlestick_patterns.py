
import pandas as pd


def validate_candles(data):
    """Validate OHLC candle data."""

    required = ["open", "high", "low", "close"]

    if not isinstance(data, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame.")

    if len(data) < 1:
        raise ValueError("At least one candle is required.")

    missing = [c for c in required if c not in data.columns]

    if missing:
        raise ValueError(f"Missing OHLC columns: {missing}")

    candles = data[required].copy()

    for column in required:
        candles[column] = pd.to_numeric(
            candles[column], errors="coerce"
        )

    if candles.isnull().any().any():
        raise ValueError("Invalid OHLC values.")

    if not candles.map(
        lambda value: pd.notna(value) and abs(value) != float("inf")
    ).all().all():
        raise ValueError("OHLC values must be finite.")

    invalid = (
        (candles["high"] < candles["low"])
        | (candles["high"] < candles["open"])
        | (candles["high"] < candles["close"])
        | (candles["low"] > candles["open"])
        | (candles["low"] > candles["close"])
    )

    if invalid.any():
        raise ValueError("Invalid candle structure.")

    return candles


def _candle_parts(candle):
    """Calculate candle body and wick sizes."""

    open_price = float(candle["open"])
    high = float(candle["high"])
    low = float(candle["low"])
    close = float(candle["close"])

    body = abs(close - open_price)
    candle_range = high - low

    upper_wick = high - max(open_price, close)
    lower_wick = min(open_price, close) - low

    return {
        "body": body,
        "range": candle_range,
        "upper_wick": upper_wick,
        "lower_wick": lower_wick,
        "bullish": close > open_price,
        "bearish": close < open_price,
    }


def detect_candlestick_patterns(data, index=None):
    """
    Detect PA-005 candlestick patterns.

    index defaults to the latest candle.

    Three-candle patterns are checked using the selected
    candle and its two preceding candles.

    Pattern detection does not independently confirm
    market trend or generate a trade signal.
    """

    candles = validate_candles(data)

    if index is None:
        index = len(candles) - 1

    if not isinstance(index, int) or isinstance(index, bool):
        raise ValueError("Index must be an integer.")

    if index < 0 or index >= len(candles):
        raise ValueError("Index is outside candle data.")

    current = candles.iloc[index]
    parts = _candle_parts(current)

    body = parts["body"]
    candle_range = parts["range"]

    patterns = []

    if candle_range > 0:
        body_ratio = body / candle_range

        # Doji: very small real body.
        if body_ratio <= 0.10:
            patterns.append("DOJI")

        # Hammer: long lower wick and small upper wick.
        if (
            parts["lower_wick"] >= 2 * body
            and parts["upper_wick"] <= body
            and min(current["open"], current["close"])
            >= current["low"] + candle_range * 0.55
        ):
            patterns.append("HAMMER")

        # Shooting Star: long upper wick and small lower wick.
        if (
            parts["upper_wick"] >= 2 * body
            and parts["lower_wick"] <= body
            and max(current["open"], current["close"])
            <= current["low"] + candle_range * 0.45
        ):
            patterns.append("SHOOTING_STAR")

    # Two-candle engulfing patterns.
    if index >= 1:
        previous = candles.iloc[index - 1]
        previous_parts = _candle_parts(previous)

        previous_body_high = max(
            previous["open"], previous["close"]
        )
        previous_body_low = min(
            previous["open"], previous["close"]
        )

        current_body_high = max(
            current["open"], current["close"]
        )
        current_body_low = min(
            current["open"], current["close"]
        )

        if (
            previous_parts["bearish"]
            and parts["bullish"]
            and current_body_low <= previous_body_low
            and current_body_high >= previous_body_high
        ):
            patterns.append("BULLISH_ENGULFING")

        if (
            previous_parts["bullish"]
            and parts["bearish"]
            and current_body_low <= previous_body_low
            and current_body_high >= previous_body_high
        ):
            patterns.append("BEARISH_ENGULFING")

    # Three-candle continuation/reversal patterns.
    if index >= 2:
        first = candles.iloc[index - 2]
        second = candles.iloc[index - 1]
        third = current

        first_parts = _candle_parts(first)
        second_parts = _candle_parts(second)
        third_parts = _candle_parts(third)

        # Three White Soldiers.
        if (
            first_parts["bullish"]
            and second_parts["bullish"]
            and third_parts["bullish"]
            and first["close"] < second["close"] < third["close"]
            and second["open"] <= first["close"]
            and third["open"] <= second["close"]
        ):
            patterns.append("THREE_WHITE_SOLDIERS")

        # Three Black Crows.
        if (
            first_parts["bearish"]
            and second_parts["bearish"]
            and third_parts["bearish"]
            and first["close"] > second["close"] > third["close"]
            and second["open"] >= first["close"]
            and third["open"] >= second["close"]
        ):
            patterns.append("THREE_BLACK_CROWS")

    return {
        "index": index,
        "patterns": patterns,
        "detected": len(patterns) > 0,
        "candle_body": body,
        "candle_range": candle_range,
        "reason": (
            "Candlestick pattern(s) detected."
            if patterns
            else "No supported pattern detected."
        ),
    }
