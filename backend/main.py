"""
Global Geopolitical War Room - FastAPI Backend Server
"""

from datetime import datetime, timezone
import logging
import os
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from backend.config import get_war_room_mode, is_mock_mode
from backend.database import (
    compare_runs,
    get_all_runs,
    get_run_by_id,
    init_db,
    save_dossier_run,
)
from backend.warroom import WarRoomResponse, execute_war_room_scan

# Initialize SQLite database
init_db()

# Initialize environment variables from project root .env
ROOT_DIR = Path(__file__).resolve().parent.parent
dotenv_path = ROOT_DIR / ".env"
if dotenv_path.exists():
    load_dotenv(dotenv_path=dotenv_path)
else:
    # Also load from current working directory if available
    load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("main")

# Detect Vercel/serverless environment
IS_VERCEL = bool(os.getenv("VERCEL") or os.getenv("VERCEL_ENV"))

# Initialize FastAPI application
# In production (Vercel), disable interactive Swagger/ReDoc docs to avoid leaking internals.
# They remain accessible in local development.
app = FastAPI(
    title="Global Geopolitical War Room API",
    description="Live & Mock Geopolitical Macro-Financial Intelligence Platform",
    version="1.0.0",
    docs_url=None if IS_VERCEL else "/docs",
    redoc_url=None if IS_VERCEL else "/redoc",
    openapi_url="/openapi.json",
)

# Enable CORS for local development and modular API integrations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# Health & Operational Mode Endpoints
# ==========================================

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint returning system status and active operational mode.
    """
    current_mode = get_war_room_mode()
    return {
        "status": "ok",
        "mode": current_mode
    }


@app.get("/api/mode", status_code=status.HTTP_200_OK)
async def get_mode_info() -> Dict[str, Any]:
    """
    Returns the current operational mode of the War Room engine.
    """
    current_mode = get_war_room_mode()
    is_mock = is_mock_mode()
    description = (
        "Local Mock Intelligence Mode (No API credits or internet required)"
        if is_mock
        else "Live Real-Time OSINT Scan Mode (Global News & Flashpoint Feeds Active)"
    )
    return {
        "status": "ok",
        "mode": current_mode,
        "is_mock": is_mock,
        "live_provider": "public_osint" if not is_mock else "mock",
        "description": description
    }




@app.get("/api/credits/check", status_code=status.HTTP_200_OK)
async def check_openai_credits() -> Dict[str, Any]:
    """
    Tests whether the configured OpenAI API key has active credits.
    In Mock Mode: returns immediately - no key needed.
    In Live Mode: makes a minimal gpt-4o-mini call to verify.
    Never exposes the API key value in the response.
    """
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    is_mock = is_mock_mode()
    has_key = bool(api_key and api_key not in ("your_api_key_here", "sk-placeholder", "your_openai_api_key_here"))

    if not has_key:
        return {
            "status": "info",
            "credits_available": False,
            "mode": "mock" if is_mock else "live",
            "message": "No OpenAI API key configured in .env. Mock Mode operates offline with full fidelity."
        }

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Reply: OK"}],
            max_tokens=3,
        )
        reply = resp.choices[0].message.content.strip() if resp.choices else "OK"
        return {
            "status": "ok",
            "credits_available": True,
            "mode": "live",
            "message": "API key active with credits. Model: " + resp.model + ". Reply: " + reply
        }
    except Exception as e:
        err = str(e)
        if "insufficient_quota" in err or "credit_balance_exhausted" in err:
            return {"status": "error", "credits_available": False, "mode": "live", "message": "No credits remaining. Add credits at https://platform.openai.com/settings/organization/billing"}
        if "invalid_api_key" in err or "Incorrect API key" in err:
            return {"status": "error", "credits_available": False, "mode": "live", "message": "Invalid API key. Check OPENAI_API_KEY in .env"}
        return {"status": "error", "credits_available": False, "mode": "live", "message": f"Credits check failed: {err[:200]}"}

# ==========================================
# Real-Time Financial Market Tickers
# ==========================================

@app.get("/api/markets/tickers", status_code=status.HTTP_200_OK)
async def get_market_tickers(refresh: bool = False) -> Dict[str, Any]:
    """
    Returns real-time financial market quotes across commodities, forex, and equities.
    Supports in-memory 30-second TTL caching with optional force refresh.
    """
    try:
        from backend.market_feeds import get_live_market_tickers
        tickers = get_live_market_tickers(force_refresh=refresh)
        return {
            "status": "ok",
            "count": len(tickers),
            "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "tickers": tickers
        }
    except Exception as e:
        logger.error(f"Error fetching market tickers: {e}", exc_info=True)
        return {
            "status": "partial",
            "count": 0,
            "tickers": [],
            "error": str(e)
        }


# ==========================================
# Baseline Theaters & Strategic Chokepoints
# ==========================================

@app.get("/api/theaters/baseline", status_code=status.HTTP_200_OK)
async def get_baseline_theaters() -> Dict[str, Any]:
    """
    Returns baseline geopolitical theaters and naval chokepoint coordinates for the tactical GIS heatmap.
    """
    theaters = [
        {
            "name": "Strait of Hormuz",
            "theater": "Middle East",
            "lat": 26.56,
            "lon": 56.25,
            "threat_level": "CRITICAL",
            "type": "Naval Chokepoint",
            "summary": "Primary crude oil transit artery (approx. 20-21M bpd). Constant surveillance & naval friction.",
            "metrics": {"oil_flow": "20.5M bpd", "risk_index": "88/100"}
        },
        {
            "name": "Bab el-Mandeb & Red Sea",
            "theater": "Middle East / Horn of Africa",
            "lat": 12.58,
            "lon": 43.33,
            "threat_level": "CRITICAL",
            "type": "Naval Chokepoint",
            "summary": "Critical entrance to Suez Canal. Maritime shipping rerouting around Cape of Good Hope.",
            "metrics": {"traffic_delta": "-52%", "risk_index": "92/100"}
        },
        {
            "name": "Taiwan Strait",
            "theater": "Indo-Pacific",
            "lat": 24.47,
            "lon": 119.82,
            "threat_level": "HIGH",
            "type": "Naval Chokepoint",
            "summary": "Core global semiconductor supply chain corridor and strategic maritime boundary.",
            "metrics": {"semi_exposure": "65%", "risk_index": "82/100"}
        },
        {
            "name": "Strait of Malacca",
            "theater": "Indo-Pacific",
            "lat": 1.43,
            "lon": 102.89,
            "threat_level": "ELEVATED",
            "type": "Naval Chokepoint",
            "summary": "Connects Indian Ocean to Pacific Ocean. High container density and Asian energy conduit.",
            "metrics": {"trade_volume": "$3.5T/yr", "risk_index": "64/100"}
        },
        {
            "name": "Eastern Europe Frontline & Black Sea",
            "theater": "Eastern Europe",
            "lat": 47.98,
            "lon": 37.80,
            "threat_level": "CRITICAL",
            "type": "Conflict Zone",
            "summary": "Active conflict theater affecting agricultural commodities, fertilizer, and European energy security.",
            "metrics": {"commodity_impact": "HIGH", "risk_index": "95/100"}
        },
        {
            "name": "Suwalki Gap",
            "theater": "Eastern Europe",
            "lat": 54.20,
            "lon": 23.30,
            "threat_level": "HIGH",
            "type": "Border Flashpoint",
            "summary": "Narrow strategic land corridor between Belarus and Kaliningrad connecting Baltic states to Poland.",
            "metrics": {"defense_readiness": "DEFCON 2", "risk_index": "76/100"}
        },
        {
            "name": "Bosphorus & Dardanelles",
            "theater": "Eurasia",
            "lat": 41.11,
            "lon": 29.07,
            "threat_level": "ELEVATED",
            "type": "Naval Chokepoint",
            "summary": "Governed by Montreux Convention. Regulates naval passage between Black Sea and Mediterranean.",
            "metrics": {"grain_transit": "Significant", "risk_index": "68/100"}
        },
        {
            "name": "Panama Canal",
            "theater": "Americas",
            "lat": 9.08,
            "lon": -79.68,
            "threat_level": "MONITORED",
            "type": "Trade Corridor",
            "summary": "Transoceanic logistics artery navigating draft restrictions and climate-induced water level volatility.",
            "metrics": {"daily_transits": "32 vessels", "risk_index": "55/100"}
        }
    ]
    return {"status": "ok", "theaters": theaters}



# ==========================================
# War Room Run Endpoint
# ==========================================

@app.post("/api/warroom/run", response_model=WarRoomResponse, status_code=status.HTTP_200_OK)
@app.post("/api/run", response_model=WarRoomResponse, status_code=status.HTTP_200_OK)
async def run_war_room() -> WarRoomResponse:
    """
    Triggers the War Room intelligence scan using OpenAI Responses API with web search.
    Reads OPENAI_API_KEY securely from server-side environment variables.
    Persists result into the SQLite historical database.
    """
    try:
        logger.info("Received request to run War Room scan.")
        result = execute_war_room_scan()
        
        # Save to database
        try:
            save_dossier_run(result.model_dump())
        except Exception as db_err:
            logger.warning(f"Failed to persist dossier run to database: {db_err}")
            
        logger.info("War Room scan completed successfully.")
        return result
    except ValueError as ve:
        logger.warning(f"Configuration or validation error during War Room scan: {ve}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        logger.error(f"Unexpected error executing War Room scan: {e}", exc_info=True)
        # Never expose internal stack traces or keys
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to complete War Room intelligence scan. Please check your OpenAI API key and network connectivity."
        )


# ==========================================
# History & Run Comparison Endpoints
# ==========================================

@app.get("/api/history", status_code=status.HTTP_200_OK)
async def list_history() -> Dict[str, Any]:
    """
    Returns a list of all historical War Room runs.
    """
    runs = get_all_runs(limit=50)
    return {"status": "ok", "runs": runs, "count": len(runs)}


@app.get("/api/history/{run_id}", status_code=status.HTTP_200_OK)
async def get_history_run(run_id: int) -> Dict[str, Any]:
    """
    Returns full dossier payload for a specific past run.
    """
    run_data = get_run_by_id(run_id)
    if not run_data:
        raise HTTPException(status_code=404, detail=f"Dossier run #{run_id} not found.")
    return {"status": "ok", "dossier": run_data}


@app.get("/api/history/compare/{run_id_a}/{run_id_b}", status_code=status.HTTP_200_OK)
async def compare_history_runs(run_id_a: int, run_id_b: int) -> Dict[str, Any]:
    """
    Computes structural delta comparison between two runs (Run A as baseline, Run B as target).
    """
    try:
        diff_result = compare_runs(run_id_a, run_id_b)
        return {"status": "ok", "comparison": diff_result}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        logger.error(f"Error comparing runs #{run_id_a} and #{run_id_b}: {e}")
        raise HTTPException(status_code=500, detail="Failed to calculate run comparison delta.")


@app.post("/api/history/seed-samples", status_code=status.HTTP_200_OK)
async def seed_sample_runs() -> Dict[str, Any]:
    """
    Seeds sample historical dossiers to instantly test and demonstrate the Comparison Engine.
    """
    sample_yesterday = {
        "report_date": "2026-09-29",
        "executive_summary": "Global markets were operating in a baseline containment regime with moderate Red Sea maritime friction and steady oil risk premiums.",
        "top_events": [
            {
                "title": "Red Sea Commercial Transit Advisory",
                "region": "Middle East",
                "severity": "HIGH",
                "summary": "Commercial shipping routes operating under heightened maritime escort advisories.",
                "impact": "Freight container rates +12% week-on-week."
            }
        ],
        "event_lifecycle": [
            {
                "event": "Red Sea Shipping Disruption",
                "stage": "Emerging",
                "momentum": "Stable",
                "details": "Naval escorts maintaining commercial corridor viability."
            },
            {
                "event": "Eastern European Frontline Friction",
                "stage": "Escalating",
                "momentum": "Stable",
                "details": "Positional artillery engagements along the eastern perimeter."
            }
        ],
        "asset_impact": [
            {"asset_class": "Crude Oil (Brent/WTI)", "bias": "NEUTRAL", "magnitude": "MEDIUM", "driver": "Adequate OPEC+ spare capacity balancing demand headwinds."},
            {"asset_class": "Gold & Silver", "bias": "BULLISH", "magnitude": "MEDIUM", "driver": "Central bank sovereign gold reserve accumulation."},
            {"asset_class": "US Dollar (DXY)", "bias": "BULLISH", "magnitude": "LOW", "driver": "Modest Treasury yield support."},
            {"asset_class": "Global Equities (S&P 500)", "bias": "NEUTRAL", "magnitude": "LOW", "driver": "Corporate earnings resilient amid stable interest rate expectations."}
        ],
        "scenarios": [
            {"scenario": "Contained Maritime Friction", "probability": "70%", "trigger": "No direct military escalation.", "market_consequence": "Rangebound commodity prices."}
        ],
        "outlook_24_72h": "Monitoring naval patrol schedules.",
        "outlook_7d": "OPEC+ technical committee discussions.",
        "what_changed": "Baseline security parameters steady.",
        "hotspots": [
            {"name": "Strait of Hormuz", "theater": "Middle East", "lat": 26.56, "lon": 56.25, "threat_level": "ELEVATED", "type": "Naval Chokepoint", "summary": "Normal commercial tanker flow under monitoring."},
            {"name": "Bab el-Mandeb & Red Sea", "theater": "Middle East", "lat": 12.58, "lon": 43.33, "threat_level": "HIGH", "type": "Naval Chokepoint", "summary": "Heightened convoy alerts."}
        ],
        "key_dates": [{"date": "2026-10-01", "event": "OPEC+ Policy Review", "importance": "HIGH"}],
        "sources": [{"name": "Reuters Macro Feed", "url": "https://reuters.com"}]
    }

    sample_today = {
        "report_date": "2026-09-30",
        "executive_summary": "Geopolitical risk premium surged sharply following sudden escalation in Strait of Hormuz patrols, triggering aggressive flight-to-safety across energy, precious metals, and sovereign bonds.",
        "top_events": [
            {
                "title": "Strait of Hormuz Naval Interdiction Flare",
                "region": "Middle East",
                "severity": "CRITICAL",
                "summary": "Sudden naval drone surveillance encounters and warning shots reported near Larak Island.",
                "impact": "Brent crude spiked +4.2%, VLCC tanker insurance war risk premiums surged 300%."
            }
        ],
        "event_lifecycle": [
            {
                "event": "Red Sea Shipping Disruption",
                "stage": "Escalating",
                "momentum": "Accelerating",
                "details": "Multiple commercial carriers suspended transits indefinitely."
            },
            {
                "event": "Eastern European Frontline Friction",
                "stage": "Escalating",
                "momentum": "Accelerating",
                "details": "Major deep-strike infrastructure drone campaign reported."
            }
        ],
        "asset_impact": [
            {"asset_class": "Crude Oil (Brent/WTI)", "bias": "BULLISH", "magnitude": "HIGH", "driver": "Imminent supply disruption risk across 20M bpd corridor."},
            {"asset_class": "Gold & Silver", "bias": "BULLISH", "magnitude": "HIGH", "driver": "Unprecedented safe-haven inflows and sovereign risk hedging."},
            {"asset_class": "US Dollar (DXY)", "bias": "BEARISH", "magnitude": "MEDIUM", "driver": "Energy cost drag and stagflationary dollar headwinds."},
            {"asset_class": "Global Equities (S&P 500)", "bias": "BEARISH", "magnitude": "HIGH", "driver": "Risk-off equity liquidation and energy inflation shock."}
        ],
        "scenarios": [
            {"scenario": "Regional Energy Escalation", "probability": "60%", "trigger": "Tanker seizure or maritime shutdown.", "market_consequence": "Oil breaks $95/bbl, global equities drop 3-5%."}
        ],
        "outlook_24_72h": "Emergency UN Security Council meeting and US Central Command alert level revision.",
        "outlook_7d": "Diplomatic backchannel negotiations through Oman and Qatar.",
        "what_changed": "Risk posture flipped from Contained to High Alert; Brent Crude bias changed from Neutral to Strong Bullish; Equities reversed from Neutral to Bearish.",
        "hotspots": [
            {"name": "Strait of Hormuz", "theater": "Middle East", "lat": 26.56, "lon": 56.25, "threat_level": "CRITICAL", "type": "Naval Chokepoint", "summary": "Active naval friction zone with highest risk weighting."},
            {"name": "Bab el-Mandeb & Red Sea", "theater": "Middle East", "lat": 12.58, "lon": 43.33, "threat_level": "CRITICAL", "type": "Naval Chokepoint", "summary": "Complete rerouting of container vessels around Africa."}
        ],
        "key_dates": [
            {"date": "2026-10-01", "event": "UNSC Emergency Session", "importance": "CRITICAL"},
            {"date": "2026-10-02", "event": "OPEC+ Emergency Quota Review", "importance": "HIGH"}
        ],
        "sources": [{"name": "Bloomberg Terminal", "url": "https://bloomberg.com"}]
    }

    id_a = save_dossier_run(sample_yesterday)
    id_b = save_dossier_run(sample_today)
    return {
        "status": "ok",
        "message": "Sample historical runs successfully seeded!",
        "seeded_run_ids": [id_a, id_b]
    }



# ==========================================
# Custom Exception Handlers for Clean Errors
# ==========================================

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": "error", "message": exc.detail},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled server exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "An unexpected server error occurred while processing the War Room analysis."
        },
    )


# ==========================================
# Mount Frontend Static Assets
# Serves the institutional command HUD on both local dev and Vercel.
# On Vercel the lambda package includes the frontend/ directory, so the
# absolute path derived from __file__ resolves correctly at runtime.

frontend_dir = ROOT_DIR / "frontend"
if frontend_dir.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")
else:
    logger.warning(f"Frontend directory not found at {frontend_dir}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
