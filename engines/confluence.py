
VALID_DIRECTIONS = {"BULLISH", "BEARISH"}

DEFAULT_CONFIRMATIONS = (
    "mtf_alignment",
    "market_structure",
    "liquidity_sweep",
    "inducement",
    "order_block",
    "fvg",
    "premium_discount",
    "candle_confirmation",
)


def evaluate_confluence(
    direction,
    confirmations,
    required_confirmations=None,
    minimum_confirmations=3,
):
    """
    Evaluate directional confluence.

    Confirmation values can be:
        True / False
        "BULLISH" / "BEARISH" / "NEUTRAL"

    Boolean values must already represent confirmation
    for the requested direction.

    Directional strings are checked against the requested
    direction.

    This engine does not independently detect market events.
    It evaluates results supplied by other engines.
    """

    if not isinstance(direction, str):
        raise ValueError("Direction must be a string.")

    direction = direction.strip().upper()

    if direction not in VALID_DIRECTIONS:
        raise ValueError("Direction must be BULLISH or BEARISH.")

    if not isinstance(confirmations, dict) or not confirmations:
        raise ValueError("Confirmations must be a non-empty dictionary.")

    if required_confirmations is None:
        required_confirmations = []

    if not isinstance(required_confirmations, (list, tuple, set)):
        raise ValueError(
            "Required confirmations must be a list, tuple or set."
        )

    if not all(
        isinstance(name, str) and name.strip()
        for name in required_confirmations
    ):
        raise ValueError("Confirmation names must be non-empty strings.")

    required = list(dict.fromkeys(required_confirmations))

    if isinstance(minimum_confirmations, bool) or not isinstance(
        minimum_confirmations, int
    ):
        raise ValueError("Minimum confirmations must be an integer.")

    if minimum_confirmations < 1:
        raise ValueError("Minimum confirmations must be at least 1.")

    if minimum_confirmations > len(confirmations):
        raise ValueError(
            "Minimum confirmations cannot exceed supplied confirmations."
        )

    missing = [
        name for name in required
        if name not in confirmations
    ]

    if missing:
        raise ValueError(
            f"Missing required confirmations: {missing}"
        )

    passed = []
    failed = []

    for name, value in confirmations.items():

        if isinstance(value, bool):
            is_confirmed = value

        elif isinstance(value, str):
            normalized = value.strip().upper()

            if normalized not in {
                "BULLISH", "BEARISH", "NEUTRAL"
            }:
                raise ValueError(
                    f"Invalid directional confirmation: {name}"
                )

            is_confirmed = normalized == direction

        else:
            raise ValueError(
                f"Confirmation '{name}' must be boolean or directional text."
            )

        if is_confirmed:
            passed.append(name)
        else:
            failed.append(name)

    required_failed = [
        name for name in required
        if name not in passed
    ]

    score = len(passed)

    eligible = (
        score >= minimum_confirmations
        and not required_failed
    )

    return {
        "direction": direction,
        "score": score,
        "total_confirmations": len(confirmations),
        "minimum_required": minimum_confirmations,
        "passed": passed,
        "failed": failed,
        "required_confirmations": required,
        "required_failed": required_failed,
        "eligible": eligible,
        "status": "CONFIRMED" if eligible else "WAIT",
        "reason": (
            "Confluence requirements satisfied."
            if eligible
            else "Insufficient or conflicting confirmations."
        ),
    }
