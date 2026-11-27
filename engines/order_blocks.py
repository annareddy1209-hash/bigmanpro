
import pandas as pd


REQUIRED_COLUMNS = ["open", "high", "low", "close"]


def validate_candles(data):
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Data must be a pandas DataFrame.")

    missing = [
        column for column in REQUIRED_COLUMNS
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
        raise ValueError("Invalid OHLC values.")

    invalid = (
        (candles["high"] < candles["low"])
        | (candles["high"] < candles["open"])
        | (candles["high"] < candles["close"])
        | (candles["low"] > candles["open"])
        | (candles["low"] > candles["close"])
    )

    if invalid.any():
        raise ValueError("Invalid candle structure.")

    return candles.reset_index(drop=True)


def identify_order_block(
    data,
    bos_index,
    direction,
    bos_confirmed,
    fvg_confirmed=False,
    require_fvg=True,
    already_used=False,
    lookback=10,
    displacement_multiplier=1.5,
):
    """
    Identify a candidate order block before a confirmed BOS.

    direction:
        BULLISH = last bearish candle before bullish BOS.
        BEARISH = last bullish candle before bearish BOS.

    The caller must supply BOS and FVG confirmation.
    This function does not independently detect either.

    Displacement is measured against the average candle body
    in the preceding candles, excluding the OB candidate.
    """

    candles = validate_candles(data)

    if isinstance(bos_index, bool) or not isinstance(
        bos_index, int
    ):
        raise ValueError("BOS index must be an integer.")

    if bos_index <= 1 or bos_index >= len(candles):
        raise ValueError("Invalid BOS index.")

    side = str(direction).strip().upper()

    if side not in ("BULLISH", "BEARISH"):
        raise ValueError(
            "Direction must be BULLISH or BEARISH."
        )

    if not isinstance(bos_confirmed, bool):
        raise ValueError("bos_confirmed must be boolean.")

    if not isinstance(fvg_confirmed, bool):
        raise ValueError("fvg_confirmed must be boolean.")

    if not isinstance(require_fvg, bool):
        raise ValueError("require_fvg must be boolean.")

    if not isinstance(already_used, bool):
        raise ValueError("already_used must be boolean.")

    if isinstance(lookback, bool) or not isinstance(lookback, int):
        raise ValueError("Lookback must be an integer.")

    if lookback < 1:
        raise ValueError("Lookback must be positive.")

    try:
        multiplier = float(displacement_multiplier)
    except (TypeError, ValueError):
        raise ValueError("Invalid displacement multiplier.")

    if not pd.notna(multiplier) or multiplier <= 0:
        raise ValueError("Displacement multiplier must be positive.")

    def rejected(reason):
        return {
            "detected": False,
            "direction": side,
            "reason": reason,
            "ob_index": None,
            "zone_high": None,
            "zone_low": None,
            "displacement_ratio": None,
        }

    if not bos_confirmed:
        return rejected("BOS is not confirmed.")

    if require_fvg and not fvg_confirmed:
        return rejected("Required FVG confirmation is missing.")

    if already_used:
        return rejected("This order block was already consumed.")

    bos = candles.iloc[bos_index]

    bos_body = abs(
        float(bos["close"]) - float(bos["open"])
    )

    if side == "BULLISH":
        bos_direction_valid = bos["close"] > bos["open"]
        opposite_candle = lambda candle: (
            candle["close"] < candle["open"]
        )
    else:
        bos_direction_valid = bos["close"] < bos["open"]
        opposite_candle = lambda candle: (
            candle["close"] > candle["open"]
        )

    if not bos_direction_valid:
        return rejected("BOS candle does not match direction.")

    start = max(1, bos_index - lookback)

    candidate_indices = [
        index
        for index in range(start, bos_index)
        if opposite_candle(candles.iloc[index])
    ]

    if not candidate_indices:
        return rejected("No opposite-direction OB candle found.")

    # The most recent opposing candle before the BOS.
    ob_index = candidate_indices[-1]

    ob = candles.iloc[ob_index]
    previous = candles.iloc[ob_index - 1]

    # The OB candle must sweep the previous candle's extreme.
    if side == "BULLISH":
        swept_previous = ob["low"] < previous["low"]
    else:
        swept_previous = ob["high"] > previous["high"]

    if not swept_previous:
        return rejected(
            "OB candle did not sweep the previous candle."
        )

    # Compare BOS displacement with earlier candle bodies.
    baseline_indices = [
        index
        for index in range(max(0, ob_index - lookback), ob_index)
    ]

    if not baseline_indices:
        return rejected("Insufficient candles for displacement.")

    baseline_bodies = (
        candles.iloc[baseline_indices]["close"]
        - candles.iloc[baseline_indices]["open"]
    ).abs()

    average_body = float(baseline_bodies.mean())

    if average_body <= 0:
        return rejected("Cannot calculate displacement baseline.")

    displacement_ratio = bos_body / average_body

    if displacement_ratio < multiplier:
        return rejected("BOS displacement is insufficient.")

    return {
        "detected": True,
        "direction": side,
        "reason": "Candidate order block validated.",
        "ob_index": ob_index,
        "zone_high": float(ob["high"]),
        "zone_low": float(ob["low"]),
        "displacement_ratio": float(displacement_ratio),
        "bos_index": bos_index,
        "fvg_confirmed": fvg_confirmed,
        "swept_previous_candle": True,
        "already_used": False,
    }
