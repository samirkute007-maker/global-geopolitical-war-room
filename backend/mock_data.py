"""
Global Geopolitical War Room - Local Mock Intelligence Provider
Generates realistic, institutional-grade sample geopolitical intelligence data without external API calls or internet dependencies.
All data is clearly labeled as illustrative mock demonstration data.
"""

from datetime import datetime
from typing import Any, Dict


def get_mock_war_room_data() -> Dict[str, Any]:
    """
    Returns a comprehensive, structured mock intelligence dossier.
    """
    now = datetime.now()
    generated_at_iso = now.isoformat()
    report_date = now.strftime("%Y-%m-%d")
    report_id = f"WR-MOCK-{now.strftime('%Y%m%d')}-001"

    geopolitical_events = [
        {
            "event_name": "US–Iran Escalation & Strait of Hormuz Maritime Friction",
            "region": "Middle East / Persian Gulf",
            "lifecycle_stage": "ESCALATION",
            "severity": "CRITICAL",
            "what_happened": "Illustrative scenario: Heightened naval drone surveillance, electronic warfare jamming incidents, and warning interdictions reported near Larak Island and the Strait of Hormuz transit lanes (controlling ~20.5M bpd of maritime crude flow).",
            "transmission_mechanism": "Maritime insurance war-risk surcharge spike (+250%) → Tanker rerouting considerations via Cape of Good Hope (+14 days transit) → Prompt crude physical supply squeeze → Global refinery feedstock margin compression.",
            "earliest_impact_window": "T+0 to T+24 Hours (Immediate spike in VLCC war-risk insurance premiums and front-month Brent prompt spreads)",
            "full_impact_window": "T+48 to T+96 Hours (Supply chain rerouting, physical tanker diversion logistics, and refinery crude procurement rebalancing)",
            "peak_risk_window": "T+3 to T+7 Days (UNSC emergency debates, regional naval escort deployment, and military retaliatory posture assessment)",
            "stabilisation_window": "T+14 to T+21 Days (Diplomatic de-confliction via backchannels, multilateral maritime safety escort corridors established)",
            "recovery_window": "T+30 to T+60 Days (Gradual normalization of war-risk premiums and recovery of standard commercial shipping flow)",
            "key_triggers_to_monitor": [
                "Direct kinetic strike on commercial energy infrastructure or oil terminals",
                "Formal mining or physical closure attempts of Strait of Hormuz transit lanes",
                "IRGC naval boarding actions or commercial tanker seizures in international waters",
                "US Fifth Fleet defensive convoy activation and rules-of-engagement revisions"
            ],
            "bullish_assets": [
                "Brent Crude",
                "WTI Crude",
                "Gold",
                "US Dollar (DXY)",
                "Defense & Aerospace Equities"
            ],
            "bearish_assets": [
                "Aviation & Logistics Equities",
                "Emerging Market FX",
                "High-Beta Equities",
                "Euro (EUR/USD)"
            ],
            "confidence_level": "HIGH (Illustrative Demonstration Model)"
        },
        {
            "event_name": "Russia–Ukraine Conflict & European Energy/Agri Infrastructure Contagion",
            "region": "Eastern Europe / Black Sea",
            "lifecycle_stage": "FULL_IMPACT",
            "severity": "CRITICAL",
            "what_happened": "Illustrative scenario: Intensified long-range strike campaign targeting Danube river export terminals, Black Sea grain transport corridors, and regional power transmission grids, with reciprocal drone interdictions at western Russian oil refining hubs.",
            "transmission_mechanism": "Agricultural fertilizer & grain supply constriction → European natural gas TTF volatility → European industrial margin squeeze → Heavy fiscal defense spending and sovereign debt issuance.",
            "earliest_impact_window": "T+0 to T+12 Hours (Agricultural futures gap-up and European gas benchmark volatility spikes)",
            "full_impact_window": "T+24 to T+72 Hours (Black Sea maritime navigation safety alerts and logistics re-routing adjustments)",
            "peak_risk_window": "T+5 to T+10 Days (EU Emergency Council sanctions review and NATO border defense posture calibration)",
            "stabilisation_window": "T+3 to T+6 Weeks (Alternative overland grain export solidarity lanes fully mobilized and storage reserves tapped)",
            "recovery_window": "T+2 to T+4 Months (Replenished European gas storage inventories and seasonal trade realignments)",
            "key_triggers_to_monitor": [
                "Targeting of western transit pipeline hubs or ammonia export conduits",
                "Disruption of Black Sea grain export insurance guarantees and naval corridor safety",
                "Secondary sanctions enforcement targeting third-party maritime oil transport"
            ],
            "bullish_assets": [
                "Wheat & Corn Commodities",
                "European Gas (TTF)",
                "Fertilizer Manufacturers",
                "Gold",
                "Defense Contractors"
            ],
            "bearish_assets": [
                "EUR/USD",
                "European Industrial Equities",
                "Eastern European Sovereign Bonds"
            ],
            "confidence_level": "HIGH (Illustrative Demonstration Model)"
        },
        {
            "event_name": "US–China Strategic Competition & Technology Supply Chain Decoupling",
            "region": "Indo-Pacific / East Asia",
            "lifecycle_stage": "STRUCTURAL",
            "severity": "HIGH",
            "what_happened": "Illustrative scenario: Expanded dual-use semiconductor export controls, critical mineral export quotas (Gallium, Germanium, and Rare Earth elements), and synchronized naval air defense intercept drills in the Taiwan Strait.",
            "transmission_mechanism": "Advanced tech supply chain bifurcation → Capex reallocation to domestic foundries → Component lead-time extensions → Critical mineral inventory hoarding across defense and automotive OEMs.",
            "earliest_impact_window": "T+24 to T+48 Hours (Global semiconductor equipment equity re-rating and currency volatility in TWD/KRW)",
            "full_impact_window": "T+1 to T+3 Months (Customs enforcement bottlenecks and tech manufacturing lead-time inflation)",
            "peak_risk_window": "T+3 to T+6 Months (Retaliatory entity list designations and mineral export license halts)",
            "stabilisation_window": "T+6 to T+12 Months (Bilateral trade working-group consultations and alternative supply chain qualification)",
            "recovery_window": "Structural / Multi-Year Transition (Permanent multi-polar industrial tech architectures)",
            "key_triggers_to_monitor": [
                "Announcement of strict rare-earth export quotas and licensing restrictions",
                "Taiwan maritime quarantine drill or exclusion zone declaration",
                "Sweeping secondary sanctions on financial institutions facilitating tech transfer"
            ],
            "bullish_assets": [
                "Domestic Semiconductor Foundries & Capex",
                "Rare Earth Miners (Ex-China)",
                "Defense Tech",
                "Cybersecurity"
            ],
            "bearish_assets": [
                "Consumer Electronics Hardware",
                "Automotive OEM Supply Chains",
                "Cross-Border Tech M&A"
            ],
            "confidence_level": "MEDIUM-HIGH (Illustrative Demonstration Model)"
        },
        {
            "event_name": "India Energy Security, Oil Import Bill & USD/INR Sensitivity",
            "region": "South Asia / Indian Ocean",
            "lifecycle_stage": "NEW_SHOCK",
            "severity": "HIGH",
            "what_happened": "Illustrative scenario: Crude oil risk premium escalation threatening India's current account deficit (CAD), widening trade deficits, and exerting depreciation pressure on the Indian Rupee (USD/INR) amid foreign portfolio capital rebalancing.",
            "transmission_mechanism": "Every $10/bbl rise in crude widens India's CAD by ~0.5% of GDP → Elevated imported inflation in fuels/logistics → RBI foreign exchange reserve intervention to smooth FX volatility → Pressure on rate-sensitive domestic equities (Banks, Autos, Paints).",
            "earliest_impact_window": "T+0 to T+24 Hours (USD/INR spot pressure, OMC oil marketing margins compressed)",
            "full_impact_window": "T+3 to T+7 Days (Domestic fuel wholesale pricing pressure, bond yield hardening)",
            "peak_risk_window": "T+2 to T+4 Weeks (Monthly trade deficit balance release and MPC monetary policy stance reassessment)",
            "stabilisation_window": "T+1 to T+2 Months (Strategic petroleum reserve tapping and rupee-denominated bilateral settlement corridors)",
            "recovery_window": "T+3 to T+6 Months (Crude price mean reversion and normalization of FPI capital flows)",
            "key_triggers_to_monitor": [
                "Brent crude sustained above $90/bbl psychological threshold",
                "RBI aggressive FX intervention defense levels at critical psychological marks",
                "Russian crude discount narrowing below $4/bbl against Middle East benchmarks",
                "Foreign Portfolio Investor (FPI) equity outflow acceleration"
            ],
            "bullish_assets": [
                "Domestic Upstream Oil & Gas (ONGC/Oil India)",
                "USD/INR (Dollar Strength vs Rupee)",
                "Gold (INR Hedge)"
            ],
            "bearish_assets": [
                "Oil Marketing Companies (OMCs)",
                "Paints & Specialty Chemicals",
                "Aviation (IndiGo)",
                "BANK NIFTY",
                "NIFTY 50 (Short-term)"
            ],
            "confidence_level": "HIGH (Illustrative Demonstration Model)"
        }
    ]

    # Map to top_events for backward compatibility
    top_events = [
        {
            "title": evt["event_name"],
            "region": evt["region"],
            "severity": evt["severity"],
            "summary": evt["what_happened"],
            "impact": evt["transmission_mechanism"]
        }
        for evt in geopolitical_events
    ]

    # Event lifecycle tracking
    event_lifecycle = [
        {
            "event": "US–Iran & Strait of Hormuz Friction",
            "stage": "ESCALATION",
            "momentum": "Accelerating",
            "details": "Naval drone encounters and maritime insurance risk premiums surging across Persian Gulf corridors."
        },
        {
            "event": "Russia–Ukraine Infrastructure Contagion",
            "stage": "FULL_IMPACT",
            "momentum": "Stable",
            "details": "High-intensity energy and transit infrastructure strikes impacting Black Sea trade and European gas."
        },
        {
            "event": "US–China Tech & Indo-Pacific Friction",
            "stage": "STRUCTURAL",
            "momentum": "Stable",
            "details": "Multi-year semiconductor decoupling, critical mineral export controls, and naval posturing."
        },
        {
            "event": "India Energy Security & USD/INR Shock",
            "stage": "NEW_SHOCK",
            "momentum": "Accelerating",
            "details": "Crude import bill inflation and trade deficit expansion creating immediate currency and rate pressure."
        }
    ]

    # 10 Required Assets with strict directional analysis
    asset_impact = [
        {
            "asset_name": "Gold",
            "asset_class": "Gold (XAU/USD)",
            "direction": "BULLISH",
            "bias": "BULLISH",
            "short_term_outlook": "Consolidating near all-time highs with strong safe-haven bids on geopolitical headline risks.",
            "seven_day_scenario": "Testing upper resistance as sovereign central bank accumulation and flight-to-safety flows accelerate.",
            "main_driver": "Sovereign safe-haven reserve demand and geopolitical tail-risk hedging.",
            "driver": "Sovereign safe-haven reserve demand and geopolitical tail-risk hedging.",
            "risk_level": "MEDIUM",
            "magnitude": "HIGH",
            "confidence": "HIGH",
            "explanation": "Gold functions as the premier non-sovereign hedge against maritime shipping escalation, stagflationary energy shocks, and currency debasement."
        },
        {
            "asset_name": "Silver",
            "asset_class": "Silver (XAG/USD)",
            "direction": "BULLISH",
            "bias": "BULLISH",
            "short_term_outlook": "High-beta co-movement with gold, supported by precious metal momentum.",
            "seven_day_scenario": "Volatile upside expansion driven by retail momentum and green energy industrial demand floor.",
            "main_driver": "Dual safe-haven correlation with gold alongside resilient industrial photovoltaic demand.",
            "driver": "Dual safe-haven correlation with gold alongside resilient industrial photovoltaic demand.",
            "risk_level": "HIGH",
            "magnitude": "HIGH",
            "confidence": "MEDIUM",
            "explanation": "Silver exhibits strong safe-haven correlation with gold but carries higher industrial beta and supply elasticity."
        },
        {
            "asset_name": "Brent Crude",
            "asset_class": "Crude Oil (Brent)",
            "direction": "BULLISH",
            "bias": "BULLISH",
            "short_term_outlook": "Geopolitical risk premium expansion of $4-$7/bbl priced into front-month contracts.",
            "seven_day_scenario": "Prompt-spread backwardation steepening as refiners seek immediate cargo loading guarantees.",
            "main_driver": "Strait of Hormuz naval friction and heightened tanker war-risk insurance surcharges.",
            "driver": "Strait of Hormuz naval friction and heightened tanker war-risk insurance surcharges.",
            "risk_level": "HIGH",
            "magnitude": "HIGH",
            "confidence": "HIGH",
            "explanation": "Immediate physical delivery fears in the Persian Gulf drive front-month prompt spread backwardation and physical cargo hoarding."
        },
        {
            "asset_name": "WTI Crude",
            "asset_class": "Crude Oil (WTI)",
            "direction": "BULLISH",
            "bias": "BULLISH",
            "short_term_outlook": "Tracking Brent higher with slight Brent-WTI spread widening.",
            "seven_day_scenario": "US Gulf Coast crude export demand surging to substitute for disrupted Middle Eastern barrels.",
            "main_driver": "US crude export arbitrage pull as international refiners bid for Atlantic Basin supply.",
            "driver": "US crude export arbitrage pull as international refiners bid for Atlantic Basin supply.",
            "risk_level": "HIGH",
            "magnitude": "HIGH",
            "confidence": "HIGH",
            "explanation": "US crude export terminals experience heightened demand pull as European refiners seek alternative non-chokepoint barrels."
        },
        {
            "asset_name": "DXY",
            "asset_class": "US Dollar Index (DXY)",
            "direction": "BULLISH",
            "bias": "BULLISH",
            "short_term_outlook": "Safe-haven dollar demand supporting the index above key moving averages.",
            "seven_day_scenario": "Liquidity hoarding preference keeping dollar elevated against G10 and emerging market peers.",
            "main_driver": "Global flight-to-safety and interest rate divergence against energy-dependent European and Asian currencies.",
            "driver": "Global flight-to-safety and interest rate divergence against energy-dependent European and Asian currencies.",
            "risk_level": "MEDIUM",
            "magnitude": "MEDIUM",
            "confidence": "HIGH",
            "explanation": "The US dollar acts as the primary global reserve haven during systemic geopolitical escalations, drawing capital away from high-beta currencies."
        },
        {
            "asset_name": "EUR/USD",
            "asset_class": "Euro (EUR/USD)",
            "direction": "BEARISH",
            "bias": "BEARISH",
            "short_term_outlook": "Downward pressure driven by European energy terms-of-trade degradation.",
            "seven_day_scenario": "Testing key psychological support levels as energy import bills widen the eurozone trade deficit.",
            "main_driver": "European energy terms-of-trade deterioration and geographical proximity to Eastern European friction.",
            "driver": "European energy terms-of-trade deterioration and geographical proximity to Eastern European friction.",
            "risk_level": "MEDIUM",
            "magnitude": "MEDIUM",
            "confidence": "HIGH",
            "explanation": "Higher energy import bills weaken the eurozone current account balance and weigh directly on the single currency."
        },
        {
            "asset_name": "GBP/USD",
            "asset_class": "British Pound (GBP/USD)",
            "direction": "BEARISH",
            "bias": "BEARISH",
            "short_term_outlook": "Stagflationary drag as energy costs complicate the Bank of England's policy path.",
            "seven_day_scenario": "Weakness against the US Dollar amid risk-off equity sentiment and UK trade sensitivity.",
            "main_driver": "UK imported energy inflation constraining Bank of England monetary policy flexibility.",
            "driver": "UK imported energy inflation constraining Bank of England monetary policy flexibility.",
            "risk_level": "MEDIUM",
            "magnitude": "MEDIUM",
            "confidence": "MEDIUM",
            "explanation": "Sterling faces pressure from terms-of-trade degradation and risk-off asset liquidation across global institutional portfolios."
        },
        {
            "asset_name": "USD/INR",
            "asset_class": "Indian Rupee (USD/INR)",
            "direction": "BULLISH",
            "bias": "BULLISH",
            "short_term_outlook": "Upward pressure on USD/INR (Rupee depreciation bias) from elevated oil marketing dollar bids.",
            "seven_day_scenario": "Testing RBI intervention bands as trade deficit expands; RBI deploying FX reserves to cap excessive volatility.",
            "main_driver": "High crude oil import dependency (~85%) widening trade deficit and driving dollar demand by oil importers.",
            "driver": "High crude oil import dependency (~85%) widening trade deficit and driving dollar demand by oil importers.",
            "risk_level": "HIGH",
            "magnitude": "HIGH",
            "confidence": "HIGH",
            "explanation": "Oil marketing companies increase dollar purchases for crude imports, while RBI deploys FX reserves to manage excessive volatility."
        },
        {
            "asset_name": "NIFTY 50",
            "asset_class": "Indian Equities (NIFTY 50)",
            "direction": "BEARISH",
            "bias": "BEARISH",
            "short_term_outlook": "Risk-off consolidation with rotational divergence between domestic defensives and energy-sensitive cyclicals.",
            "seven_day_scenario": "Defensive rotation favoring IT and Pharma while Paints, Auto, and Consumer Discretionary face margin compression.",
            "main_driver": "Higher energy input costs, FPI capital outflows, and imported inflation headwinds.",
            "driver": "Higher energy input costs, FPI capital outflows, and imported inflation headwinds.",
            "risk_level": "MEDIUM",
            "magnitude": "MEDIUM",
            "confidence": "HIGH",
            "explanation": "Indian headline equities face valuation headwinds from crude-driven inflation and emerging market risk-off rotations, partially cushioned by domestic DII institutional inflows."
        },
        {
            "asset_name": "BANK NIFTY",
            "asset_class": "Indian Financials (BANK NIFTY)",
            "direction": "BEARISH",
            "bias": "BEARISH",
            "short_term_outlook": "Underperformance relative to broader indices due to bond yield hardening and rate-cut deferral expectations.",
            "seven_day_scenario": "Net interest margin (NIM) compression concerns and higher treasury mark-to-market yields capping upside.",
            "main_driver": "Bond yield hardening dampening treasury gains and deferring RBI policy easing cycle.",
            "driver": "Bond yield hardening dampening treasury gains and deferring RBI policy easing cycle.",
            "risk_level": "HIGH",
            "magnitude": "HIGH",
            "confidence": "HIGH",
            "explanation": "Elevated crude prices delay interest rate easing cycles, keeping funding costs elevated and dampening retail credit growth momentum."
        }
    ]

    # 3 Structured Scenarios
    scenarios = [
        {
            "scenario_name": "Base Case: Contained Frictional Stalemate",
            "scenario": "Base Case: Contained Frictional Stalemate",
            "probability": "60%",
            "trigger": "Naval posturing and diplomatic signaling without permanent chokepoint closure or direct great-power kinetic engagement.",
            "geopolitical_development": "Intermittent naval interdictions and electronic warfare incidents managed via backchannel diplomacy; regional conflicts remain localized.",
            "oil_impact": "Brent crude trades in a $78–$86/bbl range with a persistent $4–$6/bbl geopolitical risk premium.",
            "usd_impact": "DXY remains firm in the 103–105 range on safe-haven liquidity preference.",
            "gold_impact": "Gold remains well-supported near record highs ($2,650–$2,750/oz) on sustained sovereign central bank accumulation.",
            "indian_market_impact": "USD/INR held steady by active RBI interventions in 83.50–84.20 range; NIFTY 50 rangebound with outperformance in Upstream Energy and IT.",
            "what_would_invalidate": "Full diplomatic ceasefire agreement, or conversely, a direct missile strike on major energy export infrastructure.",
            "market_consequence": "Rangebound commodity prices with sector-specific rotation into energy exporters and defensive havens."
        },
        {
            "scenario_name": "Escalation Case: Chokepoint Interdiction & Kinetic Spread",
            "scenario": "Escalation Case: Chokepoint Interdiction & Kinetic Spread",
            "probability": "25%",
            "trigger": "Confirmed military strike on oil refining/loading infrastructure or physical closure/mining of the Strait of Hormuz.",
            "geopolitical_development": "Multi-theater kinetic escalation involving regional powers, severe maritime shipping shutdown in the Persian Gulf and Red Sea.",
            "oil_impact": "Brent crude spikes violently past $105–$120/bbl on severe supply-side deficit fears (20M bpd at risk).",
            "usd_impact": "Broad-based US Dollar surge (DXY 107+) as institutional cash moves aggressively to short-term US Treasury bills.",
            "gold_impact": "Parabolic rally in Gold ($3,000+/oz) and Silver as systemic tail-risk insurance is priced in globally.",
            "indian_market_impact": "Severe pressure on USD/INR (depreciation past 85.00+), sharp 5–8% correction in NIFTY 50 and BANK NIFTY, aggressive OMC margin collapse.",
            "what_would_invalidate": "Immediate coordinated naval escort intervention by international coalition, emergency SPR release by IEA nations, or rapid unilateral de-escalation.",
            "market_consequence": "Stagflationary shock across energy-importing economies; sharp equity sell-off and sovereign bond yield curve inversion."
        },
        {
            "scenario_name": "De-escalation Case: Bilateral Diplomatic Accords & Maritime Guarantees",
            "scenario": "De-escalation Case: Bilateral Diplomatic Accords & Maritime Guarantees",
            "probability": "15%",
            "trigger": "Successful mediation accords (via Switzerland/Oman/Qatar) establishing verified maritime transit safety corridors and sanctions relief talks.",
            "geopolitical_development": "Formal de-escalation agreements, phased reduction of military alert levels, resumption of commercial shipping insurance guarantees.",
            "oil_impact": "Geopolitical risk premium evaporates; Brent crude corrects quickly back to $68–$74/bbl fundamentals.",
            "usd_impact": "DXY softens towards 101–102 as global risk appetite rebounds and capital flows back into emerging markets.",
            "gold_impact": "Tactical profit-taking pull-back in Gold ($2,400–$2,500/oz range) as hedge demand subsides.",
            "indian_market_impact": "Rupee strengthens sharply towards 82.80–83.20; broad relief rally across NIFTY 50, BANK NIFTY, Auto, Paint, and Aviation sectors.",
            "what_would_invalidate": "Hardline faction spoiler attacks, breakdown of ceasefire verification terms, or unexpected naval incident at sea.",
            "market_consequence": "Aggressive risk-on rotation into emerging market equities, growth stocks, and high-beta cyclical currencies."
        }
    ]

    watchlist = [
        "VLCC Persian Gulf to East Asia Tanker Freight Rates (TD3C Index)",
        "Strait of Hormuz Daily Vessel Transits & AIS Signal Disruption Density",
        "Brent-WTI Prompt Spread Backwardation / Contango Structure",
        "US Strategic Petroleum Reserve (SPR) Inventory Levels & Refill Mandates",
        "RBI Weekly Foreign Exchange Reserves & Spot FX Intervention Tranches",
        "USD/INR 1-Month Implied Volatility Surface & Forward Premia",
        "Black Sea & Red Sea War-Risk Commercial Hull Insurance Surcharges",
        "US Treasury 10Y-2Y Sovereign Yield Curve Slope & Real Rate Dynamics"
    ]

    video_script = """[0:00 - 0:15] SCENE 1: HOOK & THEATER ALERT (Presenter on Camera)
"Welcome to the Global Geopolitical War Room. Today, energy security flashpoints are flashing red. Strait of Hormuz naval tensions have triggered a sharp spike in maritime war-risk insurance, putting over twenty million barrels of daily crude flow on heightened alert."

[0:15 - 0:40] SCENE 2: MACRO TRANSMISSION (Graphic Overlay: Crude Oil & DXY Charts)
"Here is the transmission mechanism: prompt crude spreads are steepening into backwardation as refiners rush to secure physical barrels. At the same time, the US Dollar Index is catching a flight-to-safety bid against the Euro and Sterling, while Gold consolidates near record highs as institutional sovereign reserve hedging accelerates."

[0:40 - 0:65] SCENE 3: INDIA & EMERGING MARKET EXPOSURE (Graphic Overlay: USD/INR & NIFTY Heatmap)
"For emerging markets—especially India—every ten-dollar rise in crude expands the current account deficit by fifty basis points. We are seeing immediate upward pressure on USD/INR, testing the Reserve Bank's intervention lines, while Dalal Street sees defensive rotation into IT and upstream oil, with margin pressure on banking, paints, and autos."

[0:65 - 0:90] SCENE 4: 7-DAY ACTION PLAN (Presenter on Camera)
"Over the next seven days, monitor three critical triggers: first, physical tanker transits through Hormuz; second, weekly RBI foreign exchange reserve data; and third, any emergency diplomatic backchannels in Geneva. Stay disciplined, manage cross-asset risk, and subscribe to the War Room for daily briefings."
"""

    disclaimer = "MOCK DEMONSTRATION DATA: All prices, events, projections, geopolitical scenarios, and market impacts presented in this dossier are illustrative mock demonstration data for technical testing and operational evaluation. They do not represent verified current news, real-time intelligence feeds, or investment/trading advice."

    hotspots = [
        {
            "name": "Strait of Hormuz",
            "theater": "Middle East",
            "lat": 26.56,
            "lon": 56.25,
            "threat_level": "CRITICAL",
            "type": "Naval Chokepoint",
            "summary": "Primary crude oil transit artery (approx. 20.5M bpd). Heightened naval surveillance and war-risk premiums.",
            "metrics": {"oil_flow": "20.5M bpd", "risk_index": "94/100"}
        },
        {
            "name": "Bab el-Mandeb & Red Sea",
            "theater": "Middle East / Horn of Africa",
            "lat": 12.58,
            "lon": 43.33,
            "threat_level": "CRITICAL",
            "type": "Naval Chokepoint",
            "summary": "Entrance to Suez Canal. Commercial container traffic rerouting around Cape of Good Hope.",
            "metrics": {"traffic_delta": "-54%", "risk_index": "91/100"}
        },
        {
            "name": "Taiwan Strait",
            "theater": "Indo-Pacific",
            "lat": 24.47,
            "lon": 119.82,
            "threat_level": "HIGH",
            "type": "Naval Chokepoint",
            "summary": "Core global semiconductor supply chain corridor and strategic maritime boundary.",
            "metrics": {"semi_exposure": "65%", "risk_index": "84/100"}
        },
        {
            "name": "Strait of Malacca",
            "theater": "Indo-Pacific",
            "lat": 1.43,
            "lon": 102.89,
            "threat_level": "ELEVATED",
            "type": "Naval Chokepoint",
            "summary": "Connects Indian Ocean to Pacific Ocean. High container density and Asian energy conduit.",
            "metrics": {"trade_volume": "$3.5T/yr", "risk_index": "65/100"}
        },
        {
            "name": "Eastern Europe Frontline & Black Sea",
            "theater": "Eastern Europe",
            "lat": 47.98,
            "lon": 37.80,
            "threat_level": "CRITICAL",
            "type": "Conflict Zone",
            "summary": "Active conflict theater affecting agricultural commodities, fertilizer, and European energy security.",
            "metrics": {"commodity_impact": "HIGH", "risk_index": "96/100"}
        },
        {
            "name": "Suwalki Gap",
            "theater": "Eastern Europe",
            "lat": 54.20,
            "lon": 23.30,
            "threat_level": "HIGH",
            "type": "Border Flashpoint",
            "summary": "Narrow strategic land corridor between Belarus and Kaliningrad connecting Baltic states to Poland.",
            "metrics": {"defense_readiness": "DEFCON 2", "risk_index": "78/100"}
        },
        {
            "name": "Arabian Sea Energy Transit Corridor",
            "theater": "South Asia / Indian Ocean",
            "lat": 18.90,
            "lon": 69.50,
            "threat_level": "ELEVATED",
            "type": "Energy Hub",
            "summary": "Indian crude import tanker lanes and offshore production facilities off Mumbai High.",
            "metrics": {"import_density": "85% dependency", "risk_index": "72/100"}
        }
    ]

    key_dates = [
        {
            "date": f"{report_date}",
            "event": "War Room Intelligence Review & Chokepoint Assessment",
            "importance": "CRITICAL"
        },
        {
            "date": "2026-10-04",
            "event": "OPEC+ Joint Ministerial Monitoring Committee (JMMC) Strategy Meeting",
            "importance": "HIGH"
        },
        {
            "date": "2026-10-08",
            "event": "Reserve Bank of India (RBI) Monetary Policy Committee (MPC) Decision",
            "importance": "CRITICAL"
        },
        {
            "date": "2026-10-15",
            "event": "UN Security Council Maritime Security Open Debate on Strategic Chokepoints",
            "importance": "HIGH"
        }
    ]

    sources = [
        {"name": "Illustrative OSINT Maritime Tracking Feeds", "url": "https://marinetraffic.com"},
        {"name": "Simulated Macroeconomic Energy Flow Analytics", "url": "https://iea.org"},
        {"name": "Mock Geopolitical Crisis Assessment Wire", "url": "https://reuters.com"},
        {"name": "Synthetic Financial Market Cross-Asset Engine", "url": "https://bloomberg.com"}
    ]

    return {
        "mode": "mock",
        "report_id": report_id,
        "generated_at": generated_at_iso,
        "report_date": report_date,
        "report_title": "GLOBAL GEOPOLITICAL WAR ROOM — STRATEGIC INTELLIGENCE DOSSIER",
        "market_regime": "Stagflationary Energy Friction // Defensive Safe-Haven Rotation & Emerging Market FX Sensitivity",
        "executive_summary": (
            "GLOBAL SECURITY REGIME ASSESSMENT: Geopolitical risk premiums remain elevated across multiple strategic theaters, dominated by heightened maritime friction in the Strait of Hormuz and persistent infrastructure targeting along Eastern European transit corridors. Maritime insurance war-risk premiums have expanded sharply, tightening prompt-spread physical crude availability and driving global energy benchmarks higher.\n\n"
            "CROSS-ASSET TRANSMISSION DYNAMICS: The macroeconomic transmission mechanism is expressing as a classic stagflationary impulse. Safe-haven capital continues to rotate decisively into sovereign Gold reserves and the US Dollar Index (DXY), while energy-importing currencies—notably EUR/USD, GBP/USD, and USD/INR—face terms-of-trade degradation. Front-month Brent prompt spreads remain in steep backwardation, signaling acute physical cargo hoarding by international refiners.\n\n"
            "EMERGING MARKET & INDIA FOCUS: India's high crude import dependency (~85%) creates direct balance-of-payments sensitivity. Elevated imported fuel costs are widening the monthly trade deficit and creating persistent Rupee depreciation pressure on USD/INR, prompting active Reserve Bank of India foreign exchange market interventions. Equity markets reflect defensive rotation, with domestic banking and cyclical valuations constrained by delayed monetary easing expectations."
        ),
        "geopolitical_events": geopolitical_events,
        "top_events": top_events,
        "event_lifecycle": event_lifecycle,
        "asset_impact": asset_impact,
        "scenarios": scenarios,
        "watchlist": watchlist,
        "video_script": video_script,
        "disclaimer": disclaimer,
        "outlook_24_72h": "Immediate focus centers on vessel transit density in the Persian Gulf and early trading sessions across Asian energy exchanges. Watch for emergency naval patrol escort announcements and spot foreign exchange intervention by Asian central banks.",
        "outlook_7d": "Medium-term focus shifts to upcoming OPEC+ policy deliberations, emergency diplomatic backchannel communications in Muscat/Doha, and weekly sovereign petroleum inventory draw reports.",
        "what_changed": "Risk posture elevated from Contained to High Alert; Brent Crude risk premium expanded by +$5/bbl; USD/INR testing upper psychological bands; Gold safe-haven bid solidified.",
        "hotspots": hotspots,
        "key_dates": key_dates,
        "sources": sources
    }
