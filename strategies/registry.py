
# ==========================================
# BIGMAN — STRATEGY REGISTRY
# ==========================================

STRATEGIES = [
    # PRICE ACTION
    {
        "id": "PA-001",
        "name": "Supply and Demand",
        "category": "Price Action",
        "status": "Catalogued"
    },
    {
        "id": "PA-002",
        "name": "Multi-Timeframe Analysis",
        "category": "Price Action",
        "status": "Catalogued"
    },
    {
        "id": "PA-003",
        "name": "Fibonacci Retracement and Extension",
        "category": "Price Action",
        "status": "Catalogued"
    },
    {
        "id": "PA-004",
        "name": "Indicator-Free Price Action",
        "category": "Price Action",
        "status": "Catalogued"
    },
    {
        "id": "PA-005",
        "name": "Seven Candlestick Patterns",
        "category": "Price Action",
        "status": "Catalogued"
    },

    # SMART MONEY CONCEPTS
    {
        "id": "SMC-001",
        "name": "Liquidity Sweep with Structure Confirmation",
        "category": "SMC",
        "status": "Catalogued"
    },
    {
        "id": "SMC-002",
        "name": "Advanced Market Structure Mapping",
        "category": "SMC",
        "status": "Catalogued"
    },
    {
        "id": "SMC-003",
        "name": "Not Yet Submitted",
        "category": "SMC",
        "status": "Missing"
    },
    {
        "id": "SMC-004",
        "name": "Advanced Order Block Validation",
        "category": "SMC",
        "status": "Catalogued"
    },
    {
        "id": "SMC-005",
        "name": "Fair Value Gap Validation",
        "category": "SMC",
        "status": "Catalogued"
    },
    {
        "id": "SMC-006",
        "name": "Premium and Discount Zones",
        "category": "SMC",
        "status": "Catalogued"
    },
    {
        "id": "SMC-007",
        "name": "Order Flow and Mitigation",
        "category": "SMC",
        "status": "Catalogued"
    },
    {
        "id": "SMC-008",
        "name": "Integrated SMC and Price Action Reading",
        "category": "SMC",
        "status": "Catalogued"
    },
    {
        "id": "SMC-009",
        "name": "Inducement and IDM",
        "category": "SMC",
        "status": "Catalogued"
    },
    {
        "id": "SMC-010",
        "name": "Mitigation Block and Pattern Context",
        "category": "SMC",
        "status": "Catalogued"
    },
    {
        "id": "SMC-011",
        "name": "Liquidity and Inducement Confluence",
        "category": "SMC",
        "status": "Catalogued"
    },

    # RISK MANAGEMENT
    {
        "id": "RM-001",
        "name": "Risk Management and Risk-to-Reward",
        "category": "Risk Management",
        "status": "Catalogued"
    }
]


def get_all_strategies():
    return STRATEGIES


def get_strategies_by_category(category):
    return [
        strategy
        for strategy in STRATEGIES
        if strategy["category"] == category
    ]


def get_strategy_by_id(strategy_id):
    for strategy in STRATEGIES:
        if strategy["id"] == strategy_id:
            return strategy

    return None


def get_strategy_counts():
    return {
        "total": len(STRATEGIES),
        "catalogued": sum(
            s["status"] == "Catalogued"
            for s in STRATEGIES
        ),
        "missing": sum(
            s["status"] == "Missing"
            for s in STRATEGIES
        )
    }
