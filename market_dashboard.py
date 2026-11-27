
import streamlit as st

from engines.market_analysis import analyze_market


ASSETS = {
    "Gold": "XAU/USD",
    "Bitcoin": "BTC/USD",
    "Ethereum": "ETH/USD",
}

TIMEFRAMES = {
    "5 Minutes": "5min",
    "15 Minutes": "15min",
    "1 Hour": "1h",
    "4 Hours": "4h",
}


def render_market_dashboard():
    st.title("📈 BIGMAN Market Analysis")
    st.caption("Gold and Crypto market data")

    try:
        api_key = st.secrets["TWELVE_DATA_API_KEY"]
    except Exception:
        st.error(
            "Twelve Data API key is missing. "
            "Add it in Streamlit App Settings → Secrets."
        )
        return

    col1, col2 = st.columns(2)

    with col1:
        asset_name = st.selectbox(
            "Select Market",
            list(ASSETS.keys()),
        )

    with col2:
        timeframe_name = st.selectbox(
            "Select Timeframe",
            list(TIMEFRAMES.keys()),
        )

    symbol = ASSETS[asset_name]
    interval = TIMEFRAMES[timeframe_name]

    if st.button("🔄 Fetch Market Data", type="primary"):
        with st.spinner("Fetching market data..."):
            try:
                result = analyze_market(
                    api_key=api_key,
                    symbol=symbol,
                    interval=interval,
                    outputsize=200,
                )

                st.session_state["bigman_market_result"] = result
                st.session_state["bigman_market_selection"] = (
                    symbol,
                    interval,
                )

            except Exception as error:
                st.error(f"Market data error: {error}")
                return

    result = st.session_state.get(
        "bigman_market_result"
    )

    selection = st.session_state.get(
        "bigman_market_selection"
    )

    if result is None or selection != (symbol, interval):
        st.info(
            "Select a market and timeframe, then press "
            "'Fetch Market Data'."
        )
        return

    st.subheader(
        f"{result['symbol']} — {timeframe_name}"
    )

    metric1, metric2, metric3 = st.columns(3)

    metric1.metric(
        "Latest Price",
        f"{result['latest_price']:,.4f}",
    )

    metric2.metric(
        "Price Change",
        f"{result['change']:+,.4f}",
    )

    metric3.metric(
        "Change %",
        f"{result['change_percent']:+.2f}%",
    )

    st.plotly_chart(
        result["chart"],
        use_container_width=True,
    )

    st.caption(
        f"Candles loaded: {result['candles_count']} | "
        "Times displayed in UTC"
    )

    with st.expander("View Raw Market Data"):
        st.dataframe(
            result["data"].tail(50),
            use_container_width=True,
        )

    st.warning(
        "Analysis and market-data display only. "
        "BIGMAN does not place live trades."
    )
