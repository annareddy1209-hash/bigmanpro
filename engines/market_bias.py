
# ==========================================
# BIGMAN — MARKET BIAS ENGINE
# Uses confirmed swing points
# ==========================================

from engines.swing_detection import detect_swing_points


VALID_BIASES = ("BULLISH", "BEARISH", "NEUTRAL")


def analyze_market_bias(
    data,
    left_bars=2,
    right_bars=2,
):
    """
    Determine directional market bias using confirmed swings.

    BULLISH:
        Latest two swing highs form Higher Highs.
        Latest two swing lows form Higher Lows.

    BEARISH:
        Latest two swing highs form Lower Highs.
        Latest two swing lows form Lower Lows.

    NEUTRAL:
        Insufficient or mixed structure.

    This function does not independently confirm BOS,
    CHoCH, protected swings, or trading entries.
    """

    swings = detect_swing_points(
        data,
        left_bars=left_bars,
        right_bars=right_bars,
    )

    swing_highs = [
        swing for swing in swings
        if swing["type"] == "swing_high"
    ]

    swing_lows = [
        swing for swing in swings
        if swing["type"] == "swing_low"
    ]

    if len(swing_highs) < 2 or len(swing_lows) < 2:
        return {
            "bias": "NEUTRAL",
            "status": "INSUFFICIENT_STRUCTURE",
            "reason": "At least two confirmed swing highs and lows are required.",
            "higher_high": None,
            "higher_low": None,
            "lower_high": None,
            "lower_low": None,
            "latest_swing_high": (
                swing_highs[-1] if swing_highs else None
            ),
            "latest_swing_low": (
                swing_lows[-1] if swing_lows else None
            ),
            "confirmed_swing_count": len(swings),
        }

    previous_high = swing_highs[-2]["price"]
    latest_high = swing_highs[-1]["price"]

    previous_low = swing_lows[-2]["price"]
    latest_low = swing_lows[-1]["price"]

    higher_high = latest_high > previous_high
    higher_low = latest_low > previous_low

    lower_high = latest_high < previous_high
    lower_low = latest_low < previous_low

    if higher_high and higher_low:
        bias = "BULLISH"
        status = "STRUCTURE_ALIGNED"
        reason = "Higher High and Higher Low confirmed."

    elif lower_high and lower_low:
        bias = "BEARISH"
        status = "STRUCTURE_ALIGNED"
        reason = "Lower High and Lower Low confirmed."

    else:
        bias = "NEUTRAL"
        status = "MIXED_STRUCTURE"
        reason = "Swing highs and lows do not confirm the same direction."

    return {
        "bias": bias,
        "status": status,
        "reason": reason,

        "higher_high": higher_high,
        "higher_low": higher_low,
        "lower_high": lower_high,
        "lower_low": lower_low,

        "previous_swing_high": previous_high,
        "latest_swing_high": swing_highs[-1],

        "previous_swing_low": previous_low,
        "latest_swing_low": swing_lows[-1],

        "confirmed_swing_count": len(swings),
    }


def get_market_bias_status():
    return {
        "engine": "Market Bias Engine",
        "status": "FOUNDATION READY",
        "method": "Confirmed swing structure",
        "bullish_rule": "Higher High + Higher Low",
        "bearish_rule": "Lower High + Lower Low",
        "neutral_rule": "Mixed or insufficient structure",
        "uses_confirmed_swings": True,
        "generates_trade_signals": False,
    }
