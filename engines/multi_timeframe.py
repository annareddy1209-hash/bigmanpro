
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
    """Evaluate three-timeframe directional alignment."""

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


def analyze_multi_timeframe(
    market_data_by_timeframe,
    preset="INTRADAY",
    left_bars=2,
    right_bars=2,
):
    """
    Automatically analyse market bias across three timeframes.

    market_data_by_timeframe example:
        {
            "4h": dataframe,
            "1h": dataframe,
            "15min": dataframe
        }

    Missing timeframe data blocks alignment.
    """

    from engines.market_bias import analyze_market_bias

    preset = str(preset).upper()

    if preset not in TIMEFRAME_PRESETS:
        raise ValueError(
            "Preset must be INTRADAY, SWING or SCALPING."
        )

    if not isinstance(market_data_by_timeframe, dict):
        raise ValueError(
            "Market data must be a dictionary of timeframe DataFrames."
        )

    htf_tf, mtf_tf, ltf_tf = TIMEFRAME_PRESETS[preset]

    timeframe_map = {
        "HTF": htf_tf,
        "MTF": mtf_tf,
        "LTF": ltf_tf,
    }

    analysis = {}
    biases = {}

    for role, timeframe in timeframe_map.items():

        market_data = market_data_by_timeframe.get(timeframe)

        if market_data is None:
            biases[role] = "NEUTRAL"

            analysis[role] = {
                "timeframe": timeframe,
                "bias": "NEUTRAL",
                "status": "MISSING_DATA",
                "reason": "Market data is unavailable.",
            }

            continue

        result = analyze_market_bias(
            market_data,
            left_bars=left_bars,
            right_bars=right_bars,
        )

        bias = normalize_bias(result["bias"])

        biases[role] = bias

        analysis[role] = {
            "timeframe": timeframe,
            **result,
            "bias": bias,
        }

    alignment = evaluate_mtf_alignment(
        htf_bias=biases["HTF"],
        mtf_bias=biases["MTF"],
        ltf_bias=biases["LTF"],
        preset=preset,
    )

    missing_data = any(
        item["status"] == "MISSING_DATA"
        for item in analysis.values()
    )

    if missing_data:
        alignment["direction"] = "NEUTRAL"
        alignment["status"] = "NOT_ALIGNED"
        alignment["aligned"] = False
        alignment["buy_allowed_by_alignment"] = False
        alignment["sell_allowed_by_alignment"] = False
        alignment["reason"] = (
            "One or more timeframe datasets are missing. "
            "Alignment cannot be confirmed."
        )

    return {
        "valid": True,
        "preset": preset,
        "timeframe_analysis": analysis,
        "alignment": alignment,
        "direction": alignment["direction"],
        "status": alignment["status"],
        "aligned": alignment["aligned"],
        "buy_allowed_by_alignment": (
            alignment["buy_allowed_by_alignment"]
        ),
        "sell_allowed_by_alignment": (
            alignment["sell_allowed_by_alignment"]
        ),
    }
