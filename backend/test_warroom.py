"""
Unit and Integration Tests for Global Geopolitical War Room in Mock and Live modes.
"""

import os
import sys
from pathlib import Path
import unittest

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fastapi.testclient import TestClient

# Ensure WAR_ROOM_MODE=mock for testing
os.environ["WAR_ROOM_MODE"] = "mock"

from backend.main import app
from backend.config import get_war_room_mode, is_mock_mode
from backend.mock_data import get_mock_war_room_data
from backend.warroom import WarRoomResponse, execute_war_room_scan


class TestWarRoomMockMode(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_config_mock_mode(self):
        self.assertEqual(get_war_room_mode(), "mock")
        self.assertTrue(is_mock_mode())

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("status"), "ok")
        self.assertEqual(data.get("mode"), "mock")

    def test_mode_endpoint(self):
        response = self.client.get("/api/mode")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get("status"), "ok")
        self.assertEqual(data.get("mode"), "mock")
        self.assertTrue(data.get("is_mock"))
        self.assertIn("Local Mock Intelligence Mode", data.get("description", ""))

    def test_run_endpoint_mock_data(self):
        response = self.client.post("/api/run")
        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Check top-level required fields
        self.assertEqual(data.get("mode"), "mock")
        self.assertTrue(bool(data.get("report_id")))
        self.assertTrue(bool(data.get("generated_at")))
        self.assertTrue(bool(data.get("report_title")))
        self.assertTrue(bool(data.get("executive_summary")))
        self.assertTrue(bool(data.get("market_regime")))
        self.assertTrue(bool(data.get("disclaimer")))
        self.assertTrue(bool(data.get("video_script")))

        # Check Geopolitical Events (4 required)
        events = data.get("geopolitical_events", [])
        self.assertGreaterEqual(len(events), 4)
        event_names = [e.get("event_name") for e in events]
        self.assertTrue(any("Iran" in name or "Hormuz" in name for name in event_names))
        self.assertTrue(any("Ukraine" in name or "Russia" in name for name in event_names))
        self.assertTrue(any("China" in name for name in event_names))
        self.assertTrue(any("India" in name or "INR" in name for name in event_names))

        for evt in events:
            self.assertIn("lifecycle_stage", evt)
            self.assertIn(evt["lifecycle_stage"], ["NEW_SHOCK", "ESCALATION", "FULL_IMPACT", "STABILISATION", "RECOVERY", "STRUCTURAL"])
            self.assertTrue(bool(evt.get("what_happened")))
            self.assertTrue(bool(evt.get("transmission_mechanism")))
            self.assertTrue(bool(evt.get("earliest_impact_window")))
            self.assertTrue(bool(evt.get("full_impact_window")))
            self.assertTrue(bool(evt.get("peak_risk_window")))
            self.assertTrue(bool(evt.get("stabilisation_window")))
            self.assertTrue(bool(evt.get("recovery_window")))
            self.assertIsInstance(evt.get("key_triggers_to_monitor"), list)
            self.assertIsInstance(evt.get("bullish_assets"), list)
            self.assertIsInstance(evt.get("bearish_assets"), list)
            self.assertTrue(bool(evt.get("confidence_level")))

        # Check Asset Impact (10 required assets)
        assets = data.get("asset_impact", [])
        self.assertGreaterEqual(len(assets), 10)
        required_assets = [
            "Gold", "Silver", "Brent Crude", "WTI Crude",
            "DXY", "EUR/USD", "GBP/USD", "USD/INR",
            "NIFTY 50", "BANK NIFTY"
        ]
        found_asset_names = [a.get("asset_name") for a in assets]
        for req in required_assets:
            self.assertIn(req, found_asset_names, f"Asset '{req}' missing from asset_impact table")

        for asset in assets:
            self.assertTrue(bool(asset.get("direction")))
            self.assertTrue(bool(asset.get("short_term_outlook")))
            self.assertTrue(bool(asset.get("seven_day_scenario")))
            self.assertTrue(bool(asset.get("main_driver")))
            self.assertTrue(bool(asset.get("risk_level")))
            self.assertTrue(bool(asset.get("confidence")))
            self.assertTrue(bool(asset.get("explanation")))

        # Check Scenarios (3 required: Base, Escalation, De-escalation)
        scenarios = data.get("scenarios", [])
        self.assertEqual(len(scenarios), 3)
        scenario_names = [s.get("scenario_name", "") for s in scenarios]
        self.assertTrue(any("Base" in name for name in scenario_names))
        self.assertTrue(any("Escalation" in name for name in scenario_names))
        self.assertTrue(any("De-escalation" in name for name in scenario_names))

        for sc in scenarios:
            self.assertTrue(bool(sc.get("trigger")))
            self.assertTrue(bool(sc.get("geopolitical_development")))
            self.assertTrue(bool(sc.get("oil_impact")))
            self.assertTrue(bool(sc.get("usd_impact")))
            self.assertTrue(bool(sc.get("gold_impact")))
            self.assertTrue(bool(sc.get("indian_market_impact")))
            self.assertTrue(bool(sc.get("what_would_invalidate")))

        # Check Watchlist
        watchlist = data.get("watchlist", [])
        self.assertGreaterEqual(len(watchlist), 5)

        # Check Baseline Theaters Endpoint
        theaters_res = self.client.get("/api/theaters/baseline")
        self.assertEqual(theaters_res.status_code, 200)
        self.assertGreaterEqual(len(theaters_res.json().get("theaters", [])), 5)


if __name__ == "__main__":
    unittest.main()
