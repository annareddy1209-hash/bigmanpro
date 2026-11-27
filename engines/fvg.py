
import pandas as pd


def validate_candles(data):
    """Validate OHLC candle data."""

    required = ["open", "high", "low", "close"]

    if not isinstance(data, pd.DataFrame):
        raise ValueError("Input must be a pandas DataFrame.")

    if data.empty or len(data) < 3:
        raise ValueError("At least three candles are required.")

    missing = [column for column in required if column not in data.columns]

    if missing:
        raise ValueError(f"Missing OHLC columns: {missing}")

    candles = data[required].copy()

    for column in required:
        candles[column] = pd.to_numeric(
            candles[column], errors="coerce"
        )

    if candles.isnull().any().any():
        raise ValueError("OHLC data contains invalid values.")

    if not candles.apply(
        lambda column: column.map(
            lambda value: pd.notna(value) and abs(value) != float("inf")
        )
    ).all().all():
        raise ValueError("OHLC data contains non-finite values.")

    invalid = (
        (candles["high"] < candles["low"])
        | (candles["high"] < candles["open"])
        | (candles["high"] < candles["close"])
        | (candles["low"] > candles["open"])
        | (candles["low"] > candles["close"])
    )

    if invalid.any():
        raise ValueError("Invalid candle structure detected.")

    return candles


def _is_mitigated(data, index, direction, zone_low, zone_high, mode):
    """Check whether later candles have mitigated an FVG."""

    midpoint = (zone_low + zone_high) / 2

    later_candles = data.iloc[index + 1:]

    if later_candles.empty:
        return False

    if direction == "BULLISH":

        if mode == "full":
            return bool((later_candles["low"] <= zone_low).any())

        if mode == "midpoint":
            return bool((later_candles["low"] <= midpoint).any())

        if mode == "touch":
            return bool((later_candles["low"] <= zone_high).any())

    elif direction == "BEARISH":

        if mode == "full":
            return bool((later_candles["high"] >= zone_high).any())

        if mode == "midpoint":
            return bool((later_candles["high"] >= midpoint).any())

        if mode == "touch":
            return bool((later_candles["high"] >= zone_low).any())

    return False


def identify_fvg(
    data,
    index,
    direction,
    require_unmitigated=True,
    mitigation_mode="full",
):
    """
    Identify a three-candle Fair Value Gap.

    index = third candle of the three-candle pattern.

    Bullish FVG:
        First candle high < third candle low.

    Bearish FVG:
        First candle low > third candle high.

    mitigation_mode:
        full     = price completely fills the gap
        midpoint = price reaches the 50% level
        touch    = price enters the gap
    """

    candles = validate_candles(data)

    direction = str(direction).upper()
    mitigation_mode = str(mitigation_mode).lower()

    if direction not in ["BULLISH", "BEARISH"]:
        raise ValueError("Direction must be BULLISH or BEARISH.")

    if mitigation_mode not in ["full", "midpoint", "touch"]:
        raise ValueError(
            "mitigation_mode must be full, midpoint, or touch."
        )

    if not isinstance(index, int) or isinstance(index, bool):
        raise ValueError("Index must be an integer.")

    if index < 2 or index >= len(candles):
        raise ValueError("Index must identify a valid third candle.")

    first = candles.iloc[index - 2]
    third = candles.iloc[index]

    if direction == "BULLISH":

        zone_low = float(first["high"])
        zone_high = float(third["low"])

        if zone_high <= zone_low:
            return {
                "detected": False,
                "reason": "No bullish three-candle imbalance."
            }

    else:

        zone_low = float(third["high"])
        zone_high = float(first["low"])

        if zone_high <= zone_low:
            return {
                "detected": False,
                "reason": "No bearish three-candle imbalance."
            }

    mitigated = _is_mitigated(
        candles,
        index,
        direction,
        zone_low,
        zone_high,
        mitigation_mode,
    )

    if require_unmitigated and mitigated:
        return {
            "detected": False,
            "reason": "FVG has already been mitigated.",
            "mitigated": True,
            "zone_low": zone_low,
            "zone_high": zone_high,
        }

    midpoint = (zone_low + zone_high) / 2

    return {
        "detected": True,
        "direction": direction,
        "index": index,
        "zone_low": zone_low,
        "zone_high": zone_high,
        "midpoint": midpoint,
        "gap_size": zone_high - zone_low,
        "mitigated": mitigated,
        "mitigation_mode": mitigation_mode,
        "reason": "Valid three-candle FVG detected.",
    }


def scan_fvgs(
    data,
    direction=None,
    require_unmitigated=True,
    mitigation_mode="full",
):
    """Scan candle history for bullish and/or bearish FVGs."""

    candles = validate_candles(data)

    if direction is not None:
        direction = str(direction).upper()

        if direction not in ["BULLISH", "BEARISH"]:
            raise ValueError("Invalid direction.")

        directions = [direction]
    else:
        directions = ["BULLISH", "BEARISH"]

    results = []

    for index in range(2, len(candles)):

        for current_direction in directions:

            result = identify_fvg(
                candles,
                index,
                current_direction,
                require_unmitigated=require_unmitigated,
                mitigation_mode=mitigation_mode,
            )

            if result["detected"]:
                results.append(result)

    return results
