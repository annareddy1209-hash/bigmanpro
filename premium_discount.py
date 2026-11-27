
import math


def _validate_price(value, name):
    """Validate a finite numeric price."""

    if isinstance(value, bool):
        raise ValueError(f"{name} must be a valid number.")

    try:
        value = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be a valid number.")

    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite.")

    return value


def calculate_premium_discount(
    current_price,
    dealing_range_high,
    dealing_range_low,
    direction=None,
):
    """
    Calculate premium, discount and equilibrium.

    The dealing range must be supplied by a separate
    market-structure or swing-detection module.

    Bullish bias:
        Discount = favorable location to investigate buys.
        Premium = unfavorable location for fresh buys.

    Bearish bias:
        Premium = favorable location to investigate sells.
        Discount = unfavorable location for fresh sells.

    This function identifies location only.
    It does not generate a trade signal.
    """

    current_price = _validate_price(
        current_price, "Current price"
    )

    range_high = _validate_price(
        dealing_range_high, "Dealing range high"
    )

    range_low = _validate_price(
        dealing_range_low, "Dealing range low"
    )

    if range_high <= range_low:
        raise ValueError(
            "Dealing range high must be greater than range low."
        )

    if current_price < range_low or current_price > range_high:
        raise ValueError(
            "Current price must be inside the dealing range."
        )

    if direction is not None:
        direction = str(direction).upper()

        if direction not in ["BULLISH", "BEARISH"]:
            raise ValueError(
                "Direction must be BULLISH or BEARISH."
            )

    equilibrium = (range_high + range_low) / 2
    range_size = range_high - range_low

    if current_price > equilibrium:
        location = "PREMIUM"

    elif current_price < equilibrium:
        location = "DISCOUNT"

    else:
        location = "EQUILIBRIUM"

    position_percent = (
        (current_price - range_low) / range_size
    ) * 100

    if direction == "BULLISH":
        favorable_location = location == "DISCOUNT"

    elif direction == "BEARISH":
        favorable_location = location == "PREMIUM"

    else:
        favorable_location = None

    return {
        "valid": True,
        "current_price": current_price,
        "range_high": range_high,
        "range_low": range_low,
        "equilibrium": equilibrium,
        "range_size": range_size,
        "location": location,
        "position_percent": position_percent,
        "direction": direction,
        "favorable_location": favorable_location,
        "reason": (
            f"Price is in {location} of the supplied dealing range."
        ),
    }
