import os
from datetime import datetime
import requests
import streamlit as st

NEWS_API_KEY = os.getenv("NEWSDATA_API_KEY", "")
NEWS_COUNTRY = os.getenv("NEWS_COUNTRY", "us")
NEWS_CATEGORY = os.getenv("NEWS_CATEGORY", "business")
FX_BASE = os.getenv("FX_BASE", "USD")
FX_SYMBOLS = os.getenv("FX_SYMBOLS", "TWD,JPY,EUR")

st.set_page_config(page_title="Finance News Intelligence Agent", layout="wide")
st.title("Finance News Intelligence Agent")
st.caption("News + FX snapshot (Newsdata.io + open.er-api.com)")

def fetch_news():
    if not NEWS_API_KEY:
        return {"error": "Missing NEWSDATA_API_KEY"}
    url = "https://newsdata.io/api/1/news"
    params = {
        "apikey": NEWS_API_KEY,
        "country": NEWS_COUNTRY,
        "category": NEWS_CATEGORY,
        "language": "en",
    }
    r = requests.get(url, params=params, timeout=15)
    return r.json()

def fetch_fx():
    url = f"https://open.er-api.com/v6/latest/{FX_BASE}"
    r = requests.get(url, timeout=15)
    return r.json()

def parse_symbols(symbols_str: str):
    return [s.strip().upper() for s in symbols_str.split(",") if s.strip()]

col1, col2 = st.columns([2, 1])

with col2:
    st.subheader("FX Snapshot")
    fx = fetch_fx()
    if fx.get("result") == "success" and "rates" in fx:
        st.write(f"Base: **{FX_BASE}**")
        wanted = parse_symbols(FX_SYMBOLS)
        for sym in wanted:
            if sym in fx["rates"]:
                v = fx["rates"][sym]
                st.metric(label=sym, value=f"{float(v):.4f}")
            else:
                st.warning(f"Missing rate for {sym}")
        st.caption(f"Updated: {fx.get('time_last_update_utc', '-')}")
    else:
        st.error(f"Failed to fetch FX data: {fx}")

with col1:
    st.subheader("Latest Business News")
    news = fetch_news()
    if "results" in news:
        results = news["results"][:10]
        for i, item in enumerate(results, 1):
            title = item.get("title", "No title")
            link = item.get("link", "")
            source = item.get("source_id", "unknown")
            pub = item.get("pubDate", "")
            desc = item.get("description", "")
            st.markdown(f"### {i}. {title}")
            st.write(f"**Source:** {source} | **Published:** {pub}")
            if desc:
                st.write(desc[:300] + ("..." if len(desc) > 300 else ""))
            if link:
                st.markdown(f"[Read more]({link})")
            st.divider()
    else:
        st.error(f"Failed to fetch news: {news}")

st.caption(f"Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
