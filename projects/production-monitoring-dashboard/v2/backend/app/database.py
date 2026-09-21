import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "production.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def connect():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS samples (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            temp_a REAL NOT NULL,
            temp_b REAL NOT NULL,
            dirty_level REAL NOT NULL,
            clean_level REAL NOT NULL,
            flow_rate REAL NOT NULL,
            current_density REAL NOT NULL,
            output_kg REAL NOT NULL,
            availability REAL NOT NULL,
            performance REAL NOT NULL,
            quality REAL NOT NULL,
            oee REAL NOT NULL
        )
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS alarms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            severity TEXT NOT NULL,
            source TEXT NOT NULL,
            message TEXT NOT NULL,
            acknowledged INTEGER NOT NULL DEFAULT 0
        )
        """)

def insert_sample(sample: dict):
    with connect() as conn:
        conn.execute(
            """INSERT INTO samples (
                timestamp,temp_a,temp_b,dirty_level,clean_level,flow_rate,current_density,
                output_kg,availability,performance,quality,oee
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (
                sample["timestamp"], sample["temp_a"], sample["temp_b"],
                sample["dirty_level"], sample["clean_level"], sample["flow_rate"],
                sample["current_density"], sample["output_kg"], sample["availability"],
                sample["performance"], sample["quality"], sample["oee"]
            ),
        )

def insert_alarm(alarm: dict):
    with connect() as conn:
        conn.execute(
            "INSERT INTO alarms (timestamp,severity,source,message) VALUES (?,?,?,?)",
            (alarm["timestamp"], alarm["severity"], alarm["source"], alarm["message"]),
        )

def history(limit=120):
    with connect() as conn:
        rows = conn.execute(
            "SELECT * FROM samples ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(r) for r in reversed(rows)]

def alarms(limit=30):
    with connect() as conn:
        rows = conn.execute(
            "SELECT * FROM alarms ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(r) for r in rows]

def acknowledge_alarm(alarm_id: int):
    with connect() as conn:
        cur = conn.execute(
            "UPDATE alarms SET acknowledged=1 WHERE id=?", (alarm_id,)
        )
        return cur.rowcount > 0
