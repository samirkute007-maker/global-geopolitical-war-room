"""
Verify that War Room works without any OpenAI API key in mock mode.
"""

import os
import sys
from pathlib import Path
import unittest

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fastapi.testclient import TestClient

os.environ["WAR_ROOM_MODE"] = "mock"
os.environ["OPENAI_API_KEY"] = ""

from backend.main import app

class TestZeroKeyMockMode(unittest.TestCase):
    def test_run_with_empty_key(self):
        client = TestClient(app)
        response = client.post("/api/run")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["mode"], "mock")
        self.assertEqual(len(data["asset_impact"]), 10)
        self.assertEqual(len(data["geopolitical_events"]), 4)

if __name__ == "__main__":
    unittest.main()
