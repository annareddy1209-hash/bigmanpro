
# ==========================================
# BIGMAN — CENTRAL CONFIGURATION
# ==========================================

APP_NAME = "BIGMAN"
APP_VERSION = "0.1"

# ------------------------------------------
# TRADING MODE
# ------------------------------------------

DEFAULT_MODE = "Paper Trading"

PAPER_TRADING_ENABLED = True
LIVE_TRADING_ENABLED = False

# ------------------------------------------
# ACCOUNT SETTINGS
# ------------------------------------------

DEFAULT_ACCOUNT_BALANCE = 10000.0

# Risk settings are provisional.
# They must be validated before actual trading.

DEFAULT_RISK_PERCENT = 1.0
MAX_RISK_PERCENT = 2.0

# ------------------------------------------
# RISK-REWARD SETTINGS
# ------------------------------------------

MINIMUM_RISK_REWARD = 2.0

# ------------------------------------------
# STRATEGY SETTINGS
# ------------------------------------------

PRICE_ACTION_STRATEGIES = 5
SMC_STRATEGIES = 10
RISK_MANAGEMENT_STRATEGIES = 1

TOTAL_STRATEGIES = (
    PRICE_ACTION_STRATEGIES
    + SMC_STRATEGIES
    + RISK_MANAGEMENT_STRATEGIES
)

# ------------------------------------------
# MARKET SETTINGS
# ------------------------------------------

SUPPORTED_ASSETS = [
    "EURUSD",
    "GBPUSD",
    "XAUUSD",
    "BTCUSD"
]

DEFAULT_TIMEFRAMES = [
    "4H",
    "1H",
    "15M",
    "5M"
]

# ------------------------------------------
# EXECUTION SAFETY
# ------------------------------------------

ALLOW_AUTOMATIC_ORDERS = False
REQUIRE_STOP_LOSS = True
REQUIRE_RISK_VALIDATION = True

# ------------------------------------------
# DATABASE
# ------------------------------------------

DATABASE_NAME = "bigman.db"

# ------------------------------------------
# SYSTEM STATUS
# ------------------------------------------

MARKET_DATA_CONNECTED = False
STRATEGY_ENGINE_ENABLED = False
BACKTESTING_ENABLED = False
