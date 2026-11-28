"""
BIGMAN Trading Intelligence System
Central Configuration

Paper trading and market analysis only.
Live orders remain disabled.
"""

APP_NAME = "BIGMAN"
APP_VERSION = "1.0.0"

# Trading safety
TRADING_MODE = "PAPER"
LIVE_ORDERS_ENABLED = False

# Market data provider
MARKET_DATA_PROVIDER = "TWELVE_DATA"

# API key is stored securely in Streamlit Secrets
TWELVE_DATA_API_KEY_NAME = "TWELVE_DATA_API_KEY"

# Supported trading instruments
SUPPORTED_SYMBOLS = {
    "Gold": "XAU/USD",
    "Bitcoin": "BTC/USD",
    "Ethereum": "ETH/USD",
    "Zcash": "ZEC/USDT",
}

# Crypto instruments
CRYPTO_SYMBOLS = [
    "BTC/USD",
    "ETH/USD",
    "ZEC/USDT",
]

# Forex and commodity instruments
OTHER_SYMBOLS = [
    "XAU/USD",
]

# Supported chart intervals
SUPPORTED_INTERVALS = [
    "5min",
    "15min",
    "1h",
    "4h",
]

# Default chart settings
DEFAULT_SYMBOL = "XAU/USD"
DEFAULT_INTERVAL = "15min"
DEFAULT_CANDLE_LIMIT = 200

# Risk management
DEFAULT_RISK_PERCENT = 1.0
MAX_RISK_PERCENT = 2.0

# Risk reward
DEFAULT_RISK_REWARD = 2.0
MINIMUM_RISK_REWARD = 2.0

# Signal settings
MINIMUM_CONFLUENCE = 3

# Strategy settings
ENABLE_PRICE_ACTION = True
ENABLE_SMART_MONEY_CONCEPTS = True
ENABLE_MULTI_TIMEFRAME = True

# Backtesting
BACKTESTING_ENABLED = True

# Paper trading
PAPER_TRADING_ENABLED = True
PAPER_INITIAL_BALANCE = 10000.0

# Safety confirmation
REQUIRE_STOP_LOSS = True
REQUIRE_TAKE_PROFIT = True