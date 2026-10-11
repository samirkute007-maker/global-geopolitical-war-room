"""
War Room Intelligence Engine.
Supports both Local Mock Intelligence Mode (default, offline, zero API credits required)
and Live AI OSINT Scan Mode (when WAR_ROOM_MODE=live and valid OPENAI_API_KEY is configured).
"""

import json
import logging
import os
import re
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from backend.config import is_mock_mode
from backend.mock_data import get_mock_war_room_data
from backend.prompts import WAR_ROOM_SYSTEM_PROMPT, WAR_ROOM_USER_PROMPT_TEMPLATE

logger = logging.getLogger("warroom")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")


# ==========================================
# Pydantic Schemas for Strict JSON Contract
# ==========================================

class GeopoliticalEventItem(BaseModel):
    event_name: str = Field(..., description="Name of the geopolitical event or crisis")
    region: str = Field(..., description="Geographic theater (e.g. Middle East, Eastern Europe, Indo-Pacific, South Asia)")
    lifecycle_stage: str = Field(default="ESCALATION", description="NEW_SHOCK | ESCALATION | FULL_IMPACT | STABILISATION | RECOVERY | STRUCTURAL")
    severity: str = Field(default="HIGH", description="CRITICAL | HIGH | MEDIUM | ELEVATED")
    what_happened: str = Field(default="", description="Illustrative scenario of what happened")
    transmission_mechanism: str = Field(default="", description="Macroeconomic and asset transmission mechanism")
    earliest_impact_window: str = Field(default="", description="Earliest impact window")
    full_impact_window: str = Field(default="", description="Full impact window")
    peak_risk_window: str = Field(default="", description="Peak risk window")
    stabilisation_window: str = Field(default="", description="Stabilisation window")
    recovery_window: str = Field(default="", description="Recovery window")
    key_triggers_to_monitor: List[str] = Field(default_factory=list, description="Key triggers to monitor")
    bullish_assets: List[str] = Field(default_factory=list, description="Assets with bullish bias")
    bearish_assets: List[str] = Field(default_factory=list, description="Assets with bearish bias")
    confidence_level: str = Field(default="HIGH", description="Confidence level of analysis")


class TopEvent(BaseModel):
    title: str = Field(..., description="Title of the major geopolitical event or crisis")
    region: str = Field(..., description="Geographic theater")
    severity: str = Field(default="HIGH", description="CRITICAL, HIGH, MEDIUM, or ELEVATED")
    summary: str = Field(..., description="Factual breakdown of developments")
    impact: str = Field(..., description="Macroeconomic and asset transmission impact")


class EventLifecycleItem(BaseModel):
    event: str = Field(..., description="Name of the crisis / conflict / event")
    stage: str = Field(default="ESCALATION", description="NEW_SHOCK | ESCALATION | FULL_IMPACT | STABILISATION | RECOVERY | STRUCTURAL | Emerging | Escalating | Peak | De-escalating | Resolution")
    momentum: str = Field(default="Stable", description="Accelerating | Stable | Slowing")
    details: str = Field(..., description="Analysis of trajectory and escalation velocity")


class AssetImpactItem(BaseModel):
    asset_name: str = Field(default="", description="Name of specific asset (e.g., Gold, Brent Crude, USD/INR)")
    asset_class: str = Field(default="", description="Asset class identifier")
    direction: str = Field(default="VOLATILE", description="BULLISH | BEARISH | VOLATILE | NEUTRAL")
    bias: str = Field(default="VOLATILE", description="BULLISH | BEARISH | VOLATILE | NEUTRAL")
    short_term_outlook: str = Field(default="", description="Short-term outlook")
    seven_day_scenario: str = Field(default="", description="7-day forward scenario")
    main_driver: str = Field(default="", description="Primary geopolitical and macro driver")
    driver: str = Field(default="", description="Geopolitical/macro catalyst driving price action")
    risk_level: str = Field(default="MEDIUM", description="Risk level: HIGH | MEDIUM | LOW")
    magnitude: str = Field(default="MEDIUM", description="Magnitude: HIGH | MEDIUM | LOW")
    confidence: str = Field(default="HIGH", description="Confidence: HIGH | MEDIUM | LOW")
    explanation: str = Field(default="", description="Detailed institutional explanation of transmission")
    live_price: Optional[float] = Field(default=None, description="Real-time live market price")
    live_change: Optional[float] = Field(default=None, description="Real-time 24h absolute price change")
    live_change_percent: Optional[float] = Field(default=None, description="Real-time 24h percentage change")
    live_prefix: Optional[str] = Field(default="", description="Price prefix symbol (e.g. $, ₹, €)")
    live_unit: Optional[str] = Field(default="", description="Unit of measurement (e.g. USD/oz, Points)")
    live_symbol: Optional[str] = Field(default="", description="Exchange ticker symbol")
    market_status: Optional[str] = Field(default="LIVE", description="Market status")


class ScenarioItem(BaseModel):
    scenario_name: str = Field(default="", description="Scenario designation (Base Case, Escalation Case, De-escalation Case)")
    scenario: str = Field(default="", description="Scenario designation")
    probability: str = Field(default="50%", description="Estimated likelihood percentage")
    trigger: str = Field(..., description="Key catalyst or observable trigger")
    geopolitical_development: str = Field(default="", description="Expected geopolitical development")
    oil_impact: str = Field(default="", description="Impact on crude oil markets")
    usd_impact: str = Field(default="", description="Impact on US Dollar / DXY")
    gold_impact: str = Field(default="", description="Impact on Gold & precious metals")
    indian_market_impact: str = Field(default="", description="Impact on Indian markets (USD/INR, NIFTY 50, BANK NIFTY)")
    what_would_invalidate: str = Field(default="", description="What would invalidate the scenario")
    market_consequence: str = Field(default="", description="Anticipated asset and market consequences")


class KeyDateItem(BaseModel):
    date: str = Field(..., description="Date or specific timeframe")
    event: str = Field(..., description="High-stakes meeting, deadline, summit, or event")
    importance: str = Field(default="HIGH", description="CRITICAL | HIGH | MEDIUM")


class SourceItem(BaseModel):
    name: str = Field(..., description="Source name")
    url: str = Field(default="", description="Link or citation reference")


class HotspotItem(BaseModel):
    name: str = Field(..., description="Name of flashpoint or chokepoint")
    theater: str = Field(..., description="Theater region")
    lat: float = Field(..., description="Latitude coordinate")
    lon: float = Field(..., description="Longitude coordinate")
    threat_level: str = Field(default="HIGH", description="CRITICAL | HIGH | ELEVATED | MONITORED")
    type: str = Field(default="Conflict Zone", description="Naval Chokepoint | Conflict Zone | Border Flashpoint | Energy Hub")
    summary: str = Field(..., description="Tactical risk summary for this location")
    metrics: Optional[Dict[str, Any]] = Field(default=None, description="Quantitative risk metrics")


class WarRoomResponse(BaseModel):
    mode: str = Field(default="mock", description="Operational mode: 'mock' or 'live'")
    report_id: str = Field(default="", description="Unique identifier for the report")
    generated_at: str = Field(default="", description="ISO timestamp when report was generated")
    report_date: str = Field(..., description="Date of the intelligence briefing")
    report_title: str = Field(default="GLOBAL GEOPOLITICAL WAR ROOM", description="Title of the briefing report")
    market_regime: str = Field(default="", description="Macro and market regime characterization")
    executive_summary: str = Field(..., description="High-impact strategic intelligence synthesis")
    geopolitical_events: List[GeopoliticalEventItem] = Field(default_factory=list, description="Structured geopolitical events")
    top_events: List[TopEvent] = Field(default_factory=list, description="Top active geopolitical events")
    event_lifecycle: List[EventLifecycleItem] = Field(default_factory=list, description="Lifecycle status of active crises")
    asset_impact: List[AssetImpactItem] = Field(default_factory=list, description="Cross-asset impact matrix")
    scenarios: List[ScenarioItem] = Field(default_factory=list, description="Probabilistic forward-looking scenarios")
    watchlist: List[str] = Field(default_factory=list, description="Key indicators and watchpoints to monitor")
    video_script: str = Field(default="", description="90-second YouTube script for macro briefing")
    disclaimer: str = Field(default="", description="Official mock data disclaimer and advisory")
    outlook_24_72h: str = Field(..., description="24 to 72 hour tactical outlook")
    outlook_7d: str = Field(..., description="7-day medium-term strategic outlook")
    what_changed: str = Field(..., description="Key shifts and deltas in the last 24-48 hours")
    hotspots: List[HotspotItem] = Field(default_factory=list, description="Geopolitical hotspots and naval chokepoints for GIS mapping")
    key_dates: List[KeyDateItem] = Field(default_factory=list, description="Critical upcoming calendar dates")
    sources: List[SourceItem] = Field(default_factory=list, description="Referenced intelligence sources")
    market_tickers: List[Dict[str, Any]] = Field(default_factory=list, description="Real-time financial market ticker quotes")


# ==========================================
# Helpers for JSON Extraction & Sanitization
# ==========================================

def extract_json(raw_text: str) -> Dict[str, Any]:
    """
    Extracts and parses JSON object from a raw string, handling markdown wrappers.
    """
    cleaned = raw_text.strip()
    
    # Remove markdown code block fences if present
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]
        
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
        
    cleaned = cleaned.strip()
    
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        json_match = re.search(r"(\{.*\})", cleaned, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError as err:
                logger.error(f"Failed regex-extracted JSON parsing: {err}")
        raise ValueError("Could not parse valid JSON from AI response.")


def get_current_date_str() -> str:
    """Returns today's date formatted cleanly."""
    return datetime.now().strftime("%Y-%m-%d")


# ==========================================
# Core Engine: Mock & Live Execution
# ==========================================

def execute_war_room_scan(api_key: Optional[str] = None, model: Optional[str] = None) -> WarRoomResponse:
    """
    Executes War Room intelligence scan.
    
    If WAR_ROOM_MODE is 'mock' (default), returns rich local mock intelligence data
    without initializing OpenAI, making network requests, or requiring API credits.
    
    If WAR_ROOM_MODE is 'live', runs the live OpenAI Responses API scan.
    """
    from backend.market_feeds import get_live_market_tickers, enrich_asset_impacts_with_live_prices

    if is_mock_mode():
        logger.info("Executing War Room scan in MOCK MODE (local demonstration data)...")
        raw_mock = get_mock_war_room_data()
        try:
            live_tickers = get_live_market_tickers()
            raw_mock["market_tickers"] = live_tickers
            if raw_mock.get("asset_impact"):
                raw_mock["asset_impact"] = enrich_asset_impacts_with_live_prices(raw_mock["asset_impact"])
        except Exception as ticker_err:
            logger.debug(f"Ticker attachment in mock mode skipped: {ticker_err}")
        return WarRoomResponse.model_validate(raw_mock)

    # --- Live Mode Execution ---
    from backend.osint_engine import synthesize_live_war_room_dossier

    resolved_key = api_key or os.getenv("OPENAI_API_KEY", "").strip()
    has_key = bool(resolved_key and resolved_key not in ("your_api_key_here", "sk-placeholder", "your_openai_api_key_here", ""))
    provider = os.getenv("WAR_ROOM_LIVE_PROVIDER", "auto").strip().lower()

    # If user explicitly selected OSINT free feed, or has no key configured:
    if provider in ("osint", "osint_free", "rss") or not has_key:
        logger.info("Executing Live War Room scan via Public Live OSINT Feed Engine (zero credits)...")
        live_osint_data = synthesize_live_war_room_dossier()
        try:
            live_tickers = get_live_market_tickers()
            live_osint_data["market_tickers"] = live_tickers
            if live_osint_data.get("asset_impact"):
                live_osint_data["asset_impact"] = enrich_asset_impacts_with_live_prices(live_osint_data["asset_impact"])
        except Exception as ticker_err:
            logger.debug(f"Ticker attachment in OSINT mode skipped: {ticker_err}")
        return WarRoomResponse.model_validate(live_osint_data)

    # Otherwise attempt OpenAI first; if credits are exhausted, seamlessly fallback to Live OSINT Feed Engine
    try:
        from openai import OpenAI
        selected_model = model or os.getenv("OPENAI_MODEL", "gpt-4o").strip()
        current_date = get_current_date_str()
        user_prompt = WAR_ROOM_USER_PROMPT_TEMPLATE.format(current_date=current_date)
        client = OpenAI(api_key=resolved_key)
        raw_response_text = ""

        logger.info(f"Initiating Live OpenAI scan with model '{selected_model}'...")
        try:
            response = client.responses.create(
                model=selected_model,
                instructions=WAR_ROOM_SYSTEM_PROMPT,
                input=user_prompt,
                tools=[{"type": "web_search_preview"}],
            )
            if hasattr(response, "output_text") and response.output_text:
                raw_response_text = response.output_text
            elif hasattr(response, "output") and response.output:
                text_chunks = [str(getattr(item, "content", item)) for item in response.output]
                raw_response_text = "\n".join(text_chunks)
            else:
                raw_response_text = str(response)
        except Exception as resp_err:
            logger.warning(f"Responses API fallback to Chat Completions: {resp_err}")
            chat_completion = client.chat.completions.create(
                model=selected_model,
                messages=[
                    {"role": "system", "content": WAR_ROOM_SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.2,
            )
            raw_response_text = chat_completion.choices[0].message.content or ""

        if raw_response_text:
            parsed_json = extract_json(raw_response_text)
            parsed_json.setdefault("report_date", current_date)
            parsed_json.setdefault("mode", "live")
            parsed_json.setdefault("report_id", f"WR-LIVE-{datetime.now().strftime('%Y%m%d%H%M%S')}")
            parsed_json.setdefault("generated_at", datetime.now().isoformat())
            parsed_json.setdefault("disclaimer", "LIVE AI REPORT: Geopolitical intelligence synthesized via OpenAI web-search.")
            try:
                live_tickers = get_live_market_tickers()
                parsed_json["market_tickers"] = live_tickers
                if parsed_json.get("asset_impact"):
                    parsed_json["asset_impact"] = enrich_asset_impacts_with_live_prices(parsed_json["asset_impact"])
            except Exception as ticker_err:
                logger.debug(f"Ticker attachment in OpenAI live mode skipped: {ticker_err}")
            return WarRoomResponse.model_validate(parsed_json)

    except Exception as e:
        err_msg = str(e)
        logger.warning(f"OpenAI API live scan unavailable ({err_msg[:120]}). Falling back seamlessly to Public Live OSINT Engine...")
        live_osint_data = synthesize_live_war_room_dossier()
        live_osint_data["disclaimer"] = (
            "LIVE OSINT INTELLIGENCE REPORT: Synthesized from real-time global news feeds (BBC, Al Jazeera). "
            f"OpenAI credit balance was exhausted, so the Live War Room seamlessly routed through the real-time public OSINT engine."
        )
        try:
            live_tickers = get_live_market_tickers()
            live_osint_data["market_tickers"] = live_tickers
            if live_osint_data.get("asset_impact"):
                live_osint_data["asset_impact"] = enrich_asset_impacts_with_live_prices(live_osint_data["asset_impact"])
        except Exception as ticker_err:
            logger.debug(f"Ticker attachment in fallback skipped: {ticker_err}")
        return WarRoomResponse.model_validate(live_osint_data)

    # Fallback: no live data was produced (should not normally reach here)
    raw_mock = get_mock_war_room_data()
    logger.warning("War Room scan produced no result; falling back to mock data.")
    return WarRoomResponse.model_validate(raw_mock)
