
import streamlit as st
from datetime import datetime

from strategies.registry import (
    get_all_strategies,
    get_strategy_counts,
    get_strategies_by_category,
)

from market_dashboard import render_market_dashboard


# ==========================================
# BIGMAN — TRADING INTELLIGENCE TERMINAL
# ==========================================

st.set_page_config(
    page_title="BIGMAN Trading Terminal",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==========================================
# CUSTOM DESIGN
# ==========================================

st.markdown("""
<style>
.stApp {
    background-color: #0b1020;
    color: #ffffff;
}

section[data-testid="stSidebar"] {
    background-color: #11182b;
}

h1, h2, h3, p, label {
    color: #ffffff;
}

div[data-testid="stMetric"] {
    background: #151f35;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #263653;
}

.status {
    color: #20d9c4;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# LOAD STRATEGY DATA
# ==========================================

strategies = get_all_strategies()
counts = get_strategy_counts()


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("⚡ BIGMAN")
st.sidebar.caption("TRADING INTELLIGENCE SYSTEM")
st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Dashboard",
        "Strategy Repository",
        "Market Analysis",
        "Strategy Engine",
        "Trade Signals",
        "Backtesting",
        "Risk Management",
        "Trade Journal",
        "System Status",
    ],
)

st.sidebar.divider()

mode = st.sidebar.selectbox(
    "Trading Mode",
    ["Paper Trading", "Analysis Only"],
)

st.sidebar.success("LIVE ORDERS DISABLED")
st.sidebar.caption("BIGMAN | Development Build 0.3")


# ==========================================
# DASHBOARD
# ==========================================

if page == "Dashboard":

    st.title("⚡ BIGMAN")
    st.subheader(
        "Smart Money & Price Action Trading Terminal"
    )

    st.markdown(
        '<p class="status">● SYSTEM INITIALIZED | LIVE ORDERS DISABLED</p>',
        unsafe_allow_html=True,
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Catalogued Strategies",
        counts["catalogued"],
    )

    col2.metric(
        "Missing Strategies",
        counts["missing"],
    )

    col3.metric(
        "Active Signals",
        "0",
    )

    col4.metric(
        "Trading Mode",
        mode,
    )

    st.divider()

    st.subheader("Strategy Overview")

    category1, category2, category3 = st.columns(3)

    category1.metric(
        "Price Action",
        len(get_strategies_by_category("Price Action")),
    )

    category2.metric(
        "Smart Money Concepts",
        len(get_strategies_by_category("SMC")),
    )

    category3.metric(
        "Risk Management",
        len(get_strategies_by_category("Risk Management")),
    )

    st.divider()

    st.subheader("System Modules")

    modules = [
        "Market Structure Engine",
        "Liquidity Detection Engine",
        "Order Block Engine",
        "Fair Value Gap Engine",
        "Fibonacci Engine",
        "Candle Confirmation Engine",
        "Confluence Evaluator",
        "Risk Management Engine",
        "Market Data Engine",
        "Candlestick Chart Engine",
    ]

    for module in modules:
        st.write("⏳", module)

    st.divider()

    st.caption(
        "Last dashboard refresh: "
        + datetime.now().strftime("%d %B %Y, %H:%M:%S")
    )

    st.info(
        "Market-data and chart modules are integrated. "
        "Provider connectivity still needs to be tested. "
        "Trading signals are not yet enabled."
    )


# ==========================================
# STRATEGY REPOSITORY
# ==========================================

elif page == "Strategy Repository":

    st.title("📚 BIGMAN Strategy Repository")

    st.metric(
        "Catalogued Strategies",
        counts["catalogued"],
    )

    selected_category = st.selectbox(
        "Filter by category",
        [
            "All",
            "Price Action",
            "SMC",
            "Risk Management",
        ],
    )

    if selected_category == "All":
        filtered = strategies
    else:
        filtered = get_strategies_by_category(
            selected_category
        )

    for strategy in filtered:

        with st.expander(
            f"{strategy['id']} — {strategy['name']}"
        ):
            st.write(
                "Category:",
                strategy["category"],
            )

            st.write(
                "Status:",
                strategy["status"],
            )

    st.warning(
        "Catalogue entries are not yet executable trading strategies."
    )


# ==========================================
# MARKET ANALYSIS
# ==========================================

elif page == "Market Analysis":

    render_market_dashboard()


# ==========================================
# STRATEGY ENGINE
# ==========================================

elif page == "Strategy Engine":

    st.title("🧠 Strategy Engine")

    st.info(
        "Strategy implementation is pending."
    )


# ==========================================
# TRADE SIGNALS
# ==========================================

elif page == "Trade Signals":

    st.title("🎯 Trade Signals")

    st.info(
        "No trading signals are generated."
    )


# ==========================================
# BACKTESTING
# ==========================================

elif page == "Backtesting":

    st.title("🧪 Backtesting")

    st.info(
        "Historical testing engine is pending."
    )


# ==========================================
# RISK MANAGEMENT
# ==========================================

elif page == "Risk Management":

    st.title("🛡️ Risk Management")

    st.info(
        "Risk validation engine is pending."
    )


# ==========================================
# TRADE JOURNAL
# ==========================================

elif page == "Trade Journal":

    st.title("📒 Trade Journal")

    st.info(
        "Trade journal is pending."
    )


# ==========================================
# SYSTEM STATUS
# ==========================================

elif page == "System Status":

    st.title("⚙️ BIGMAN System Status")

    st.write("Application: BIGMAN")
    st.write("Version: 0.3")
    st.write("Trading mode:", mode)

    st.write(
        "Catalogued strategies:",
        counts["catalogued"],
    )

    st.write(
        "Missing strategies:",
        counts["missing"],
    )

    st.write(
        "Market data module: Integrated"
    )

    st.write(
        "Market provider: Twelve Data (connection unverified)"
    )

    st.write(
        "Chart engine: Integrated"
    )

    st.write(
        "Database: Not connected"
    )

    st.write(
        "Live orders: Disabled"
    )
