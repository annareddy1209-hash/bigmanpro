
VALID_BIASES = {"BULLISH", "BEARISH", "NEUTRAL"}


TIMEFRAME_PRESETS = {
    "INTRADAY": ("4h", "1h", "15min"),
    "SWING": ("4h", "1h", "15min"),
    "SCALPING": ("1h", "15min", "5min"),
}


def normalize_bias(bias):
    """Validate and normalize a directional market bias."""

    if not isinstance(bias, str):
        raise ValueError("Market bias must be a string.")

    normalized = bias.strip().upper()

    if normalized not in VALID_BIASES:
        raise ValueError(
            "Bias must be BULLISH, BEARISH or NEUTRAL."
        )

    return normalized


def evaluate_mtf_alignment(
    htf_bias,
    mtf_bias,
    ltf_bias,
    preset="INTRADAY",
):
    """
    Evaluate three-timeframe directional alignment.

    INTRADAY / SWING:
        HTF = 4h
        MTF = 1h
        LTF = 15min

    SCALPING:
        HTF = 1h
        MTF = 15min
        LTF = 5min

    Bias values must come from a separate validated
    market-structure analysis module.

    This function evaluates alignment only. It does not
    independently detect BOS, CHoCH or swing structure.
    """

    preset = str(preset).upper()

    if preset not in TIMEFRAME_PRESETS:
        raise ValueError(
            "Preset must be INTRADAY, SWING or SCALPING."
        )

    htf = normalize_bias(htf_bias)
    mtf = normalize_bias(mtf_bias)
    ltf = normalize_bias(ltf_bias)

    htf_timeframe, mtf_timeframe, ltf_timeframe = (
        TIMEFRAME_PRESETS[preset]
    )

    aligned_bullish = (
        htf == "BULLISH"
        and mtf == "BULLISH"
        and ltf == "BULLISH"
    )

    aligned_bearish = (
        htf == "BEARISH"
        and mtf == "BEARISH"
        and ltf == "BEARISH"
    )

    if aligned_bullish:
        direction = "BULLISH"
        status = "ALIGNED"

    elif aligned_bearish:
        direction = "BEARISH"
        status = "ALIGNED"

    else:
        direction = "NEUTRAL"
        status = "NOT_ALIGNED"

    return {
        "valid": True,
        "preset": preset,
        "timeframes": {
            "HTF": htf_timeframe,
            "MTF": mtf_timeframe,
            "LTF": ltf_timeframe,
        },
        "biases": {
            "HTF": htf,
            "MTF": mtf,
            "LTF": ltf,
        },
        "direction": direction,
        "status": status,
        "aligned": status == "ALIGNED",
        "buy_allowed_by_alignment": aligned_bullish,
        "sell_allowed_by_alignment": aligned_bearish,
        "reason": (
            f"All three timeframes align {direction}."
            if status == "ALIGNED"
            else "Timeframes are not fully aligned. Wait for confirmation."
        ),
    }
