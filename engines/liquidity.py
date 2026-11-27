
import pandas as pd


REQUIRED_COLUMNS = [
    "open",
    "high",
    "low",
    "close",
]


def validate_candles(data):
    """Validate OHLC candle data."""

    if not isinstance(data, pd.DataFrame):
        raise TypeError("Data must be a pandas DataFrame.")

    missing = [
        column
        for column in REQUIRED_COLUMNS
        if column not in data.columns
    ]

    if missing:
        raise ValueError(
            f"Missing columns: {', '.join(missing)}"
        )

    if data.empty:
        raise ValueError("Candle data is empty.")

    candles = data.copy()

    for column in REQUIRED_COLUMNS:
        candles[column] = pd.to_numeric(
            candles[column],
            errors="coerce",
        )

    if candles[REQUIRED_COLUMNS].isna().any().any():
        raise ValueError("Invalid OHLC values detected.")

    invalid = (
        (candles["high"] < candles["low"])
        | (candles["high"] < candles["open"])
        | (candles["high"] < candles["close"])
        | (candles["low"] > candles["open"])
        | (candles["low"] > candles["close"])
    )

    if invalid.any():
        raise ValueError("Invalid candle structure detected.")

    return candles.reset_index(drop=True)


def detect_liquidity_sweep(
    data,
    liquidity_level,
    liquidity_side,
):
    """
    Detect a liquidity sweep on the latest candle.

    liquidity_side:
        sell_side = price sweeps below the level
                    and closes back above it.

        buy_side  = price sweeps above the level
                    and closes back below it.

    This function identifies a price event only.
    It does not generate a trading signal.
    """

    candles = validate_candles(data)

    try:
        level = float(liquidity_level)
    except (TypeError, ValueError):
        raise ValueError("Liquidity level must be numeric.")

    if not pd.notna(level):
        raise ValueError("Liquidity level must be valid.")

    side = str(liquidity_side).strip().lower()

    if side not in ("buy_side", "sell_side"):
        raise ValueError(
            "liquidity_side must be buy_side or sell_side."
        )

    candle = candles.iloc[-1]

    open_price = float(candle["open"])
    high_price = float(candle["high"])
    low_price = float(candle["low"])
    close_price = float(candle["close"])

    swept = False
    direction = "NONE"

    if side == "sell_side":
        swept = (
            low_price < level
            and close_price > level
        )

        if swept:
            direction = "BULLISH"

    elif side == "buy_side":
        swept = (
            high_price > level
            and close_price < level
        )

        if swept:
            direction = "BEARISH"

    sweep_distance = 0.0

    if swept and side == "sell_side":
        sweep_distance = level - low_price

    elif swept and side == "buy_side":
        sweep_distance = high_price - level

    return {
        "detected": swept,
        "liquidity_side": side,
        "liquidity_level": level,
        "direction": direction,
        "sweep_distance": sweep_distance,
        "candle_open": open_price,
        "candle_high": high_price,
        "candle_low": low_price,
        "candle_close": close_price,
        "confirmation": (
            "Wick crossed level and candle closed back inside."
            if swept
            else "No confirmed sweep on latest candle."
        ),
    }


def scan_liquidity_sweeps(
    data,
    liquidity_level,
    liquidity_side,
):
    """
    Scan all candles for liquidity sweep events.
    """

    candles = validate_candles(data)

    events = []

    for index in range(len(candles)):
        result = detect_liquidity_sweep(
            candles.iloc[:index + 1],
            liquidity_level,
            liquidity_side,
        )

        if result["detected"]:
            event = result.copy()
            event["candle_index"] = index
            events.append(event)

    return events
