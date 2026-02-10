import os
import hashlib
from datetime import datetime
import requests

NEWS_API_KEY = os.getenv("NEWSDATA_API_KEY", "")
NEWS_COUNTRY = os.getenv("NEWS_COUNTRY", "us")
NEWS_CATEGORY = os.getenv("NEWS_CATEGORY", "business")
FX_BASE = os.getenv("FX_BASE", "USD")
FX_SYMBOLS = os.getenv("FX_SYMBOLS", "TWD,JPY,EUR")

OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_news():
    url = "https://newsdata.io/api/1/news"
    params = {"apikey": NEWS_API_KEY, "country": NEWS_COUNTRY, "category": NEWS_CATEGORY, "language": "en"}
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    return r.json()

def fetch_fx():
    url = "https://api.exchangerate.host/latest"
    params = {"base": FX_BASE, "symbols": FX_SYMBOLS}
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    return r.json()

def deduplicate_news(items):
    seen = set()
    out = []
    for it in items:
        key = (it.get("title", "") + it.get("link", "")).strip().lower()
        h = hashlib.sha256(key.encode("utf-8")).hexdigest()
        if h not in seen:
            seen.add(h)
            out.append(it)
    return out

def compose_html(news_items, fx_data):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fx_html = ""
    if "rates" in fx_data:
        fx_html += f"<p><b>Base:</b> {FX_BASE}</p><ul>"
        for k, v in fx_data["rates"].items():
            fx_html += f"<li>{k}: {v:.4f}</li>"
        fx_html += "</ul>"
    news_html = ""
    for i, item in enumerate(news_items[:10], 1):
        title = item.get("title", "No title")
        link = item.get("link", "")
        source = item.get("source_id", "unknown")
        pub = item.get("pubDate", "")
        desc = item.get("description", "")
        news_html += f"<h3>{i}. {title}</h3><p><b>Source:</b> {source} | <b>Published:</b> {pub}</p><p>{desc}</p><p><a href=\"{link}\">Read more</a></p><hr>"
    return f"<html><head><meta charset=\"utf-8\"></head><body><h1>Finance Digest</h1><p>Generated at {now}</p><h2>FX Snapshot</h2>{fx_html}<h2>Top Business News</h2>{news_html}</body></html>"

def main():
    if not NEWS_API_KEY:
        raise RuntimeError("Missing NEWSDATA_API_KEY")
    news_data = fetch_news()
    fx_data = fetch_fx()
    items = deduplicate_news(news_data.get("results", []))
    html = compose_html(items, fx_data)
    out_path = os.path.join(OUTPUT_DIR, "digest.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(out_path)

if __name__ == "__main__":
    main()
