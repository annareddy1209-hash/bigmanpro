
# ==========================================
# BIGMAN — MARKET STRUCTURE ENGINE
# Strategy Reference: SMC-002
# ==========================================

from engines.swing_detection import detect_swing_points

VALID_DIRECTIONS = ("bullish", "bearish")

MINIMUM_PULLBACK_PERCENT = 40.0


def is_valid_pullback(
    retracement_percent,
    minimum_percent=MINIMUM_PULLBACK_PERCENT
):
    if retracement_percent is None:
        return False

    if not 0 <= retracement_percent <= 100:
        return False

    return retracement_percent >= minimum_percent


def calculate_retracement_percent(
    impulse_start,
    impulse_end,
    pullback_price,
    direction,
):
    """
    Calculate pullback as a percentage of the impulse.

    Bullish:
        Impulse moves upward, pullback moves downward.

    Bearish:
        Impulse moves downward, pullback moves upward.
    """

    direction = direction.lower()

    if direction not in VALID_DIRECTIONS:
        raise ValueError("Invalid market direction.")

    prices = [impulse_start, impulse_end, pullback_price]

    if any(price is None for price in prices):
        raise ValueError("All price values are required.")

    if direction == "bullish":
        impulse_size = impulse_end - impulse_start
        pullback_size = impulse_end - pullback_price
    else:
        impulse_size = impulse_start - impulse_end
        pullback_size = pullback_price - impulse_end

    if impulse_size <= 0:
        raise ValueError("Invalid impulse direction or size.")

    if pullback_size < 0 or pullback_size > impulse_size:
        raise ValueError("Pullback is outside the impulse range.")

    return (pullback_size / impulse_size) * 100.0


def get_confirmed_structure_levels(
    data,
    left_bars=2,
    right_bars=2,
):
    """
    Extract the latest automatically detected,
    confirmed swing high and swing low.

    These are candidate structure levels.
    They are not automatically classified as
    protected swings or BOS levels.
    """

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
        "swing_high": latest_high,
        "swing_low": latest_low,
        "swing_count": len(swings),
        "levels_available": (
            latest_high is not None
            and latest_low is not None
        ),
    }


def confirm_bos(direction, candle_close, swing_level):
    """
    Confirm BOS using candle close.
    Wick-only breaks are rejected.
    """

    direction = direction.lower()

    if direction not in VALID_DIRECTIONS:
        raise ValueError("Direction must be bullish or bearish.")

    if candle_close is None or swing_level is None:
        return False

    if direction == "bullish":
        return candle_close > swing_level

    return candle_close < swing_level


def confirm_choch(direction, candle_close, protected_swing):
    """
    Confirm CHoCH using a protected swing break.
    """

    direction = direction.lower()

    if direction not in VALID_DIRECTIONS:
        raise ValueError("Direction must be bullish or bearish.")

    if candle_close is None or protected_swing is None:
        return False

    if direction == "bullish":
        return candle_close < protected_swing

    return candle_close > protected_swing


def evaluate_structure_event(
    direction,
    candle_close,
    swing_high,
    swing_low,
    protected_swing=None
):
    """
    Evaluate supplied structure levels.

    CHoCH is checked before BOS.
    """

    direction = direction.lower()

    if direction not in VALID_DIRECTIONS:
        raise ValueError("Invalid market direction.")

    if confirm_choch(
        direction,
        candle_close,
        protected_swing
    ):
        return "CHoCH"

    if direction == "bullish":
        if confirm_bos(
            "bullish",
            candle_close,
            swing_high
        ):
            return "BOS"

    else:
        if confirm_bos(
            "bearish",
            candle_close,
            swing_low
        ):
            return "BOS"

    return "NONE"


def get_engine_status():
    return {
        "engine": "Market Structure Engine",
        "strategy": "SMC-002",
        "status": "SWING INTEGRATION READY",
        "minimum_pullback_percent": MINIMUM_PULLBACK_PERCENT,
        "wick_only_breaks": False,
        "automatic_swing_detection": True,
        "protected_swing_detection": False,
    }
