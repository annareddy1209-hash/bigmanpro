
import math


def _positive_number(value, name):
    """Validate a positive finite number."""

    if isinstance(value, bool):
        raise ValueError(f"{name} must be numeric.")

    try:
        value = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be numeric.")

    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be positive and finite.")

    return value


def calculate_position_risk(
    account_balance,
    risk_percent,
    entry_price,
    stop_loss,
    direction,
    point_value_per_unit=1.0,
    reward_ratios=(2.0, 3.0),
    max_risk_percent=2.0,
):
    """
    Calculate theoretical position size and target prices.

    point_value_per_unit:
        Monetary value gained or lost for each one-unit
        price movement per one position unit.

        This must be supplied correctly for the broker's
        Gold or Crypto contract specification.

    This function does not place trades or submit orders.
    """

    balance = _positive_number(
        account_balance, "Account balance"
    )

    risk = _positive_number(
        risk_percent, "Risk percentage"
    )

    entry = _positive_number(
        entry_price, "Entry price"
    )

    stop = _positive_number(
        stop_loss, "Stop loss"
    )

    point_value = _positive_number(
        point_value_per_unit, "Point value per unit"
    )

    max_risk = _positive_number(
        max_risk_percent, "Maximum risk percentage"
    )

    if risk > max_risk:
        raise ValueError(
            "Risk percentage exceeds the configured maximum."
        )

    if not isinstance(direction, str):
        raise ValueError("Direction must be a string.")

    direction = direction.strip().upper()

    if direction not in ("BUY", "SELL"):
        raise ValueError("Direction must be BUY or SELL.")

    if direction == "BUY" and stop >= entry:
        raise ValueError(
            "BUY stop loss must be below entry price."
        )

    if direction == "SELL" and stop <= entry:
        raise ValueError(
            "SELL stop loss must be above entry price."
        )

    if not isinstance(reward_ratios, (list, tuple)):
        raise ValueError("Reward ratios must be a list or tuple.")

    if not reward_ratios:
        raise ValueError("At least one reward ratio is required.")

    ratios = [
        _positive_number(value, "Reward ratio")
        for value in reward_ratios
    ]

    if len(set(ratios)) != len(ratios):
        raise ValueError("Reward ratios must be unique.")

    risk_amount = balance * (risk / 100)
    stop_distance = abs(entry - stop)

    risk_per_unit = stop_distance * point_value

    position_size = risk_amount / risk_per_unit

    targets = {}

    for ratio in ratios:

        if direction == "BUY":
            target = entry + (stop_distance * ratio)
        else:
            target = entry - (stop_distance * ratio)

        if target <= 0:
            raise ValueError(
                "Calculated target price must be positive."
            )

        targets[f"TP_{ratio:g}R"] = target

    return {
        "valid": True,
        "direction": direction,
        "account_balance": balance,
        "risk_percent": risk,
        "risk_amount": risk_amount,
        "entry_price": entry,
        "stop_loss": stop,
        "stop_distance": stop_distance,
        "point_value_per_unit": point_value,
        "position_size_units": position_size,
        "reward_ratios": ratios,
        "targets": targets,
        "maximum_risk_percent": max_risk,
        "live_trading": False,
        "reason": "Risk calculations completed. No order was placed.",
    }
