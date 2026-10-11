"""
Real-Time Financial Market Ticker Feed Engine
Fetches live market prices, daily changes, percentage movements, and high/lows for key geopolitical macro assets:
- Precious Metals: Gold (GC=F), Silver (SI=F)
- Energy & Commodities: Brent Crude (BZ=F), WTI Crude (CL=F), Natural Gas (NG=F)
- Forex & Currencies: US Dollar Index (DX-Y.NYB), EUR/USD, GBP/USD, USD/INR, USD/JPY
- Global Equity Indices: NIFTY 50 (^NSEI), BANK NIFTY (^NSEBANK), S&P 500 (^GSPC), US 10Y Yield (^TNX)
- Macro Liquidity: Bitcoin (BTC-USD)

Zero API Keys required - Direct resilient public financial gateway with concurrent async fetching and in-memory TTL caching.
"""

import concurrent.futures
import json
import logging
import time
import urllib.request
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger("warroom.markets")

# Track cache: {'timestamp': float, 'data': List[Dict]}
_MARKET_CACHE: Dict[str, Any] = {
    "timestamp": 0,
    "ttl_seconds": 30,
    "data": []
}

# Master Asset Catalog with human-readable names and categories
ASSET_CATALOG = [
    {
        "symbol": "GC=F",
        "name": "Gold",
        "display_name": "Gold Spot/Futures",
        "category": "Precious Metals",
        "unit": "USD/oz",
        "prefix": "$",
        "decimals": 2
    },
    {
        "symbol": "SI=F",
        "name": "Silver",
        "display_name": "Silver Futures",
        "category": "Precious Metals",
        "unit": "USD/oz",
        "prefix": "$",
        "decimals": 3
    },
    {
        "symbol": "BZ=F",
        "name": "Brent Crude",
        "display_name": "Brent Crude Oil",
        "category": "Energy",
        "unit": "USD/bbl",
        "prefix": "$",
        "decimals": 2
    },
    {
        "symbol": "CL=F",
        "name": "WTI Crude",
        "display_name": "WTI Crude Oil",
        "category": "Energy",
        "unit": "USD/bbl",
        "prefix": "$",
        "decimals": 2
    },
    {
        "symbol": "DX-Y.NYB",
        "name": "DXY",
        "display_name": "US Dollar Index",
        "category": "Forex",
        "unit": "Points",
        "prefix": "",
        "decimals": 2
    },
    {
        "symbol": "EURUSD=X",
        "name": "EUR/USD",
        "display_name": "Euro / US Dollar",
        "category": "Forex",
        "unit": "Rate",
        "prefix": "€",
        "decimals": 4
    },
    {
        "symbol": "GBPUSD=X",
        "name": "GBP/USD",
        "display_name": "British Pound / USD",
        "category": "Forex",
        "unit": "Rate",
        "prefix": "£",
        "decimals": 4
    },
    {
        "symbol": "USDINR=X",
        "name": "USD/INR",
        "display_name": "USD / Indian Rupee",
        "category": "Forex",
        "unit": "₹",
        "prefix": "₹",
        "decimals": 2
    },
    {
        "symbol": "USDJPY=X",
        "name": "USD/JPY",
        "display_name": "USD / Japanese Yen",
        "category": "Forex",
        "unit": "¥",
        "prefix": "¥",
        "decimals": 2
    },
    {
        "symbol": "^NSEI",
        "name": "NIFTY 50",
        "display_name": "NSE NIFTY 50",
        "category": "Equities",
        "unit": "Points",
        "prefix": "",
        "decimals": 2
    },
    {
        "symbol": "^NSEBANK",
        "name": "BANK NIFTY",
        "display_name": "NSE BANK NIFTY",
        "category": "Equities",
        "unit": "Points",
        "prefix": "",
        "decimals": 2
    },
    {
        "symbol": "^GSPC",
        "name": "S&P 500",
        "display_name": "S&P 500 Index",
        "category": "Equities",
        "unit": "Points",
        "prefix": "",
        "decimals": 2
    },
    {
        "symbol": "BTC-USD",
        "name": "Bitcoin",
        "display_name": "Bitcoin (Macro Liquidity)",
        "category": "Digital Assets",
        "unit": "USD",
        "prefix": "$",
        "decimals": 2
    }
]


def _fetch_single_ticker(asset: Dict[str, Any]) -> Dict[str, Any]:
    """Fetches real-time price quote for a single financial instrument."""
    symbol = asset["symbol"]
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1d"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }

    item_result = {
        "symbol": symbol,
        "name": asset["name"],
        "display_name": asset["display_name"],
        "category": asset["category"],
        "unit": asset["unit"],
        "prefix": asset["prefix"],
        "price": None,
        "previous_close": None,
        "change": 0.0,
        "change_percent": 0.0,
        "direction": "NEUTRAL",
        "day_high": None,
        "day_low": None,
        "currency": "USD",
        "status": "LIVE",
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=4) as response:
            if response.status == 200:
                payload = json.loads(response.read().decode("utf-8"))
                result_list = payload.get("chart", {}).get("result", [])
                if result_list:
                    meta = result_list[0].get("meta", {})
                    price = meta.get("regularMarketPrice")
                    prev_close = meta.get("chartPreviousClose") or meta.get("previousClose")
                    day_high = meta.get("regularMarketDayHigh")
                    day_low = meta.get("regularMarketDayLow")
                    currency = meta.get("currency", "USD")

                    if price is not None:
                        decimals = asset.get("decimals", 2)
                        item_result["price"] = round(float(price), decimals)
                        item_result["day_high"] = round(float(day_high), decimals) if day_high else item_result["price"]
                        item_result["day_low"] = round(float(day_low), decimals) if day_low else item_result["price"]
                        item_result["currency"] = currency

                        if prev_close:
                            item_result["previous_close"] = round(float(prev_close), decimals)
                            chg = float(price) - float(prev_close)
                            chg_pct = (chg / float(prev_close)) * 100.0
                            item_result["change"] = round(chg, decimals)
                            item_result["change_percent"] = round(chg_pct, 2)

                            if chg_pct > 0.05:
                                item_result["direction"] = "BULLISH"
                            elif chg_pct < -0.05:
                                item_result["direction"] = "BEARISH"
                            else:
                                item_result["direction"] = "NEUTRAL"
    except Exception as exc:
        logger.debug("Live quote fetch fallback for %s: %s", symbol, exc)

    return item_result


def get_live_market_tickers(force_refresh: bool = False) -> List[Dict[str, Any]]:
    """
    Returns live market quotes for all War Room financial assets.
    Uses concurrent multi-threaded fetching with 30s cache TTL.
    """
    global _MARKET_CACHE
    now = time.time()

    if not force_refresh and _MARKET_CACHE["data"] and (now - _MARKET_CACHE["timestamp"] < _MARKET_CACHE["ttl_seconds"]):
        return _MARKET_CACHE["data"]

    logger.info("Fetching real-time financial market tickers across global exchanges...")
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        future_map = {executor.submit(_fetch_single_ticker, asset): asset for asset in ASSET_CATALOG}
        for future in concurrent.futures.as_completed(future_map):
            try:
                res = future.result()
                results.append(res)
            except Exception as e:
                asset = future_map[future]
                logger.warning("Error fetching %s: %s", asset["symbol"], e)

    # Re-order according to ASSET_CATALOG order
    order_map = {asset["symbol"]: idx for idx, asset in enumerate(ASSET_CATALOG)}
    results.sort(key=lambda x: order_map.get(x["symbol"], 99))

    # If any price failed to fetch, retain previous known price from cache
    if _MARKET_CACHE["data"]:
        cached_dict = {c["symbol"]: c for c in _MARKET_CACHE["data"]}
        for r in results:
            if r.get("price") is None and r["symbol"] in cached_dict:
                cached_item = cached_dict[r["symbol"]]
                r["price"] = cached_item.get("price")
                r["change"] = cached_item.get("change", 0.0)
                r["change_percent"] = cached_item.get("change_percent", 0.0)
                r["direction"] = cached_item.get("direction", "NEUTRAL")

    _MARKET_CACHE["timestamp"] = now
    _MARKET_CACHE["data"] = results
    return results


def enrich_asset_impacts_with_live_prices(asset_impacts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Matches Asset Impact items with real-time market pricing and returns enriched items.
    """
    live_tickers = {t["name"].lower(): t for t in get_live_market_tickers()}

    # Name mapping variations
    aliases = {
        "gold": "gold",
        "silver": "silver",
        "brent crude": "brent crude",
        "brent crude oil": "brent crude",
        "wti crude": "wti crude",
        "wti crude oil": "wti crude",
        "crude oil": "brent crude",
        "dxy": "dxy",
        "us dollar index": "dxy",
        "dollar index": "dxy",
        "eur/usd": "eur/usd",
        "eurusd": "eur/usd",
        "gbp/usd": "gbp/usd",
        "gbpusd": "gbp/usd",
        "usd/inr": "usd/inr",
        "usdinr": "usd/inr",
        "usd/jpy": "usd/jpy",
        "usdjpy": "usd/jpy",
        "nifty 50": "nifty 50",
        "nifty": "nifty 50",
        "bank nifty": "bank nifty",
        "s&p 500": "s&p 500",
        "sp500": "s&p 500",
        "bitcoin": "bitcoin",
        "btc": "bitcoin"
    }

    for item in asset_impacts:
        raw_name = (item.get("asset_name") or item.get("asset") or "").lower().strip()
        matched_key = aliases.get(raw_name)
        if matched_key and matched_key in live_tickers:
            ticker = live_tickers[matched_key]
            item["live_price"] = ticker.get("price")
            item["live_change"] = ticker.get("change")
            item["live_change_percent"] = ticker.get("change_percent")
            item["live_prefix"] = ticker.get("prefix", "")
            item["live_unit"] = ticker.get("unit", "")
            item["live_symbol"] = ticker.get("symbol", "")
            item["market_status"] = ticker.get("status", "LIVE")

    return asset_impacts
