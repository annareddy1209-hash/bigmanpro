
# ==========================================
# BIGMAN — MARKET STRUCTURE ENGINE
# Strategy Reference: SMC-002
# ==========================================

VALID_DIRECTIONS = ("bullish", "bearish")

# Educator-specific minimum pullback rule.
MINIMUM_PULLBACK_PERCENT = 40.0


def is_valid_pullback(
    retracement_percent,
    minimum_percent=MINIMUM_PULLBACK_PERCENT
):
    """
    Checks whether a measured pullback meets
    the SMC-002 minimum retracement requirement.

    The retracement percentage must be calculated
    by a separate, validated swing-measurement function.
    """

    if retracement_percent is None:
        return False

    if not 0 <= retracement_percent <= 100:
        return False

    return retracement_percent >= minimum_percent


def confirm_bos(direction, candle_close, swing_level):
    """
    Confirms a Break of Structure using candle close.

    Bullish BOS:
        Candle closes above previous valid swing high.

    Bearish BOS:
        Candle closes below previous valid swing low.

    Wick-only breaks are not accepted.
    """

    direction = direction.lower()

    if direction not in VALID_DIRECTIONS:
        raise ValueError("Direction must be bullish or bearish.")

    if direction == "bullish":
        return candle_close > swing_level

    return candle_close < swing_level


def confirm_choch(direction, candle_close, protected_swing):
    """
    Confirms a Change of Character.

    Bullish structure:
        Close below protected Higher Low.

    Bearish structure:
        Close above protected Lower High.
    """

    direction = direction.lower()

    if direction not in VALID_DIRECTIONS:
        raise ValueError("Direction must be bullish or bearish.")

    if protected_swing is None:
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
    Evaluates a candle against supplied valid
    structure levels.

    Returns:
        CHoCH
        BOS
        NONE

    CHoCH is checked first because a protected
    swing break signals a potential structure shift.
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
        "status": "FOUNDATION READY",
        "minimum_pullback_percent": MINIMUM_PULLBACK_PERCENT,
        "wick_only_breaks": False,
        "automatic_swing_detection": False
    }
