"""
Historical Dossier Database & Run Comparison Engine
Provides persistent SQLite storage and intelligent delta computation between War Room intelligence runs.

Serverless Compatibility:
  - Vercel and similar serverless environments use read-only filesystems.
  - This module detects such environments and falls back to /tmp (ephemeral).
  - All database operations degrade gracefully when no writable path is available.
"""

import json
import logging
import os
import sqlite3
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger("warroom.db")


def _resolve_db_path() -> Path:
    """
    Resolves the SQLite database file path, falling back to /tmp in serverless environments.
    Returns the Path object to use for the database file.
    """
    # 1. Prefer the local data/ directory (local dev)
    project_root = Path(__file__).resolve().parent.parent
    preferred_dir = project_root / "data"
    try:
        preferred_dir.mkdir(parents=True, exist_ok=True)
        test_file = preferred_dir / ".write_test"
        test_file.write_text("ok")
        test_file.unlink()
        return preferred_dir / "warroom_history.db"
    except (OSError, PermissionError):
        pass

    # 2. Serverless fallback: /tmp (ephemeral, writable on Vercel/AWS Lambda)
    tmp_dir = Path("/tmp")
    if tmp_dir.exists():
        logger.warning("Project data/ directory is read-only. Using /tmp for database (ephemeral storage).")
        return tmp_dir / "warroom_history.db"

    # 3. Final fallback: temp directory (Windows serverless edge case)
    tmp_dir = Path(tempfile.gettempdir())
    if tmp_dir.exists():
        logger.error("No project-writable path available. Using system temp dir for database (ephemeral).")
        return tmp_dir / "warroom_history.db"


DB_PATH = _resolve_db_path()
_DB_AVAILABLE = True


def get_db_connection() -> Optional[sqlite3.Connection]:
    """Creates a database connection with dict-like row factory. Returns None if DB is unavailable."""
    global _DB_AVAILABLE
    if not _DB_AVAILABLE:
        return None
    try:
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to database at {DB_PATH}: {e}")
        _DB_AVAILABLE = False
        return None


def init_db() -> None:
    """Initializes SQLite schema for historical War Room runs. Gracefully skips if DB is unavailable."""
    conn = get_db_connection()
    if conn is None:
        logger.warning("Database unavailable — skipping schema initialization.")
        return
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dossier_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                report_date TEXT NOT NULL,
                title TEXT NOT NULL,
                executive_summary TEXT,
                payload JSON NOT NULL,
                critical_events_count INTEGER DEFAULT 0,
                hotspots_count INTEGER DEFAULT 0
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_dossier_date ON dossier_runs (report_date)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_dossier_created ON dossier_runs (created_at)")
        conn.commit()
        logger.info(f"Database initialized successfully at {DB_PATH}")
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
    finally:
        conn.close()


def save_dossier_run(dossier_dict: Dict[str, Any]) -> int:
    """
    Saves a completed War Room dossier run into the SQLite database.
    Returns the inserted record ID, or -1 if database is unavailable (serverless).
    """
    conn = get_db_connection()
    if conn is None:
        logger.warning("Database unavailable — dossier run not persisted.")
        return -1
    cursor = conn.cursor()
    
    report_date = dossier_dict.get("report_date", datetime.now().strftime("%Y-%m-%d"))
    exec_summary = dossier_dict.get("executive_summary", "")
    
    # Generate a brief title from top event, geopolitical event, or report_title
    top_events = dossier_dict.get("top_events", [])
    geo_events = dossier_dict.get("geopolitical_events", [])
    if dossier_dict.get("report_title"):
        primary_title = str(dossier_dict.get("report_title"))
    elif top_events and len(top_events) > 0:
        primary_title = f"{top_events[0].get('title', 'Global Briefing')}"
    elif geo_events and len(geo_events) > 0:
        primary_title = f"{geo_events[0].get('event_name', 'Global Briefing')}"
    else:
        primary_title = f"Strategic Briefing - {report_date}"
        
    events_to_check = top_events if top_events else geo_events
    critical_count = sum(
        1 for e in events_to_check if "CRITICAL" in str(e.get("severity", "")).upper()
    )
    hotspots_count = len(dossier_dict.get("hotspots", []))
    
    payload_json = json.dumps(dossier_dict)
    
    cursor.execute("""
        INSERT INTO dossier_runs (
            created_at, report_date, title, executive_summary, payload, critical_events_count, hotspots_count
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        report_date,
        primary_title,
        exec_summary[:500] if exec_summary else "",
        payload_json,
        critical_count,
        hotspots_count
    ))
    
    inserted_id = cursor.lastrowid
    conn.commit()
    conn.close()
    logger.info(f"Saved dossier run #{inserted_id} ({report_date})")
    return inserted_id


def get_all_runs(limit: int = 50) -> List[Dict[str, Any]]:
    """Retrieves list of recent dossier runs with metadata. Returns empty list if DB unavailable."""
    conn = get_db_connection()
    if conn is None:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, created_at, report_date, title, executive_summary, critical_events_count, hotspots_count
            FROM dossier_runs
            ORDER BY id DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        results = []
        for r in rows:
            results.append({
                "id": r["id"],
                "created_at": r["created_at"],
                "report_date": r["report_date"],
                "title": r["title"],
                "executive_summary_snippet": r["executive_summary"],
                "critical_events_count": r["critical_events_count"],
                "hotspots_count": r["hotspots_count"]
            })
        return results
    except Exception as e:
        logger.error(f"Failed to retrieve runs: {e}")
        return []
    finally:
        conn.close()


def get_run_by_id(run_id: int) -> Optional[Dict[str, Any]]:
    """Retrieves full payload of a specific dossier run. Returns None if DB unavailable."""
    conn = get_db_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dossier_runs WHERE id = ?", (run_id,))
        row = cursor.fetchone()
        if not row:
            return None
        payload = json.loads(row["payload"])
        payload["_meta"] = {
            "id": row["id"],
            "created_at": row["created_at"],
            "title": row["title"],
            "critical_events_count": row["critical_events_count"],
            "hotspots_count": row["hotspots_count"]
        }
        return payload
    except Exception as e:
        logger.error(f"Failed to retrieve run #{run_id}: {e}")
        return None
    finally:
        conn.close()


def compare_runs(run_id_a: int, run_id_b: int) -> Dict[str, Any]:
    """
    Computes a detailed structural comparison & delta between two runs (Run A as baseline, Run B as target/newer).
    """
    run_a = get_run_by_id(run_id_a)
    run_b = get_run_by_id(run_id_b)
    
    if not run_a or not run_b:
        raise ValueError("One or both requested dossier runs could not be found.")
        
    # 1. Asset Impact Delta
    assets_a = {item.get("asset_class", "").strip(): item for item in run_a.get("asset_impact", [])}
    assets_b = {item.get("asset_class", "").strip(): item for item in run_b.get("asset_impact", [])}
    
    asset_changes = []
    all_asset_keys = set(assets_a.keys()).union(set(assets_b.keys()))
    
    for key in sorted(all_asset_keys):
        item_a = assets_a.get(key)
        item_b = assets_b.get(key)
        
        if item_a and item_b:
            bias_changed = item_a.get("bias") != item_b.get("bias")
            mag_changed = item_a.get("magnitude") != item_b.get("magnitude")
            if bias_changed or mag_changed or item_a.get("driver") != item_b.get("driver"):
                asset_changes.append({
                    "asset_class": key,
                    "type": "MODIFIED",
                    "bias_before": item_a.get("bias", "NEUTRAL"),
                    "bias_after": item_b.get("bias", "NEUTRAL"),
                    "magnitude_before": item_a.get("magnitude", "MEDIUM"),
                    "magnitude_after": item_b.get("magnitude", "MEDIUM"),
                    "driver_after": item_b.get("driver", "")
                })
        elif item_b and not item_a:
            asset_changes.append({
                "asset_class": key,
                "type": "NEW_ASSET",
                "bias_before": "N/A",
                "bias_after": item_b.get("bias", "NEUTRAL"),
                "magnitude_before": "N/A",
                "magnitude_after": item_b.get("magnitude", "MEDIUM"),
                "driver_after": item_b.get("driver", "")
            })
        elif item_a and not item_b:
            asset_changes.append({
                "asset_class": key,
                "type": "REMOVED",
                "bias_before": item_a.get("bias", "NEUTRAL"),
                "bias_after": "N/A",
                "magnitude_before": item_a.get("magnitude", "MEDIUM"),
                "magnitude_after": "N/A",
                "driver_after": "No longer flagged"
            })
            
    # 2. Lifecycle Shifts
    lifecycle_a = {item.get("event", "").strip(): item for item in run_a.get("event_lifecycle", [])}
    lifecycle_b = {item.get("event", "").strip(): item for item in run_b.get("event_lifecycle", [])}
    
    lifecycle_shifts = []
    for key in sorted(set(lifecycle_a.keys()).union(set(lifecycle_b.keys()))):
        item_a = lifecycle_a.get(key)
        item_b = lifecycle_b.get(key)
        
        if item_a and item_b:
            if item_a.get("stage") != item_b.get("stage") or item_a.get("momentum") != item_b.get("momentum"):
                lifecycle_shifts.append({
                    "event": key,
                    "stage_before": item_a.get("stage"),
                    "stage_after": item_b.get("stage"),
                    "momentum_before": item_a.get("momentum"),
                    "momentum_after": item_b.get("momentum"),
                    "details": item_b.get("details", "")
                })
        elif item_b and not item_a:
            lifecycle_shifts.append({
                "event": key,
                "stage_before": "N/A",
                "stage_after": item_b.get("stage"),
                "momentum_before": "N/A",
                "momentum_after": item_b.get("momentum"),
                "details": item_b.get("details", "")
            })

    # 3. Hotspot Threat Level Shifts
    hotspots_a = {item.get("name", "").strip(): item for item in run_a.get("hotspots", [])}
    hotspots_b = {item.get("name", "").strip(): item for item in run_b.get("hotspots", [])}
    
    hotspot_shifts = []
    for key in sorted(set(hotspots_a.keys()).union(set(hotspots_b.keys()))):
        item_a = hotspots_a.get(key)
        item_b = hotspots_b.get(key)
        
        if item_a and item_b:
            if item_a.get("threat_level") != item_b.get("threat_level"):
                hotspot_shifts.append({
                    "name": key,
                    "threat_before": item_a.get("threat_level"),
                    "threat_after": item_b.get("threat_level"),
                    "summary": item_b.get("summary", "")
                })
        elif item_b and not item_a:
            hotspot_shifts.append({
                "name": key,
                "threat_before": "NEW",
                "threat_after": item_b.get("threat_level"),
                "summary": item_b.get("summary", "")
            })

    return {
        "run_a": {
            "id": run_a.get("_meta", {}).get("id", run_id_a),
            "date": run_a.get("report_date", ""),
            "title": run_a.get("_meta", {}).get("title", ""),
            "created_at": run_a.get("_meta", {}).get("created_at", "")
        },
        "run_b": {
            "id": run_b.get("_meta", {}).get("id", run_id_b),
            "date": run_b.get("report_date", ""),
            "title": run_b.get("_meta", {}).get("title", ""),
            "created_at": run_b.get("_meta", {}).get("created_at", "")
        },
        "what_changed_today_b": run_b.get("what_changed", ""),
        "asset_changes": asset_changes,
        "lifecycle_shifts": lifecycle_shifts,
        "hotspot_shifts": hotspot_shifts,
        "summary_delta": {
            "summary_a": run_a.get("executive_summary", ""),
            "summary_b": run_b.get("executive_summary", "")
        }
    }


# Auto-initialize database schema on module import
init_db()
