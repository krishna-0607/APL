from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Dict, List


class PowerStore:
    def __init__(self, sqlite_path: str):
        self.path = Path(sqlite_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path)
        self._create_schema()

    def _create_schema(self) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS custom_powers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                primary_color TEXT NOT NULL,
                secondary_color TEXT NOT NULL,
                particle_profile TEXT NOT NULL,
                sound_profile TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.commit()

    def upsert_power(self, power: Dict[str, str]) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT INTO custom_powers(name, primary_color, secondary_color, particle_profile, sound_profile)
            VALUES(?,?,?,?,?)
            ON CONFLICT(name) DO UPDATE SET
              primary_color=excluded.primary_color,
              secondary_color=excluded.secondary_color,
              particle_profile=excluded.particle_profile,
              sound_profile=excluded.sound_profile
            """,
            (
                power["name"],
                power["primary_color"],
                power["secondary_color"],
                power["particle_profile"],
                power["sound_profile"],
            ),
        )
        self.conn.commit()

    def list_powers(self) -> List[Dict[str, str]]:
        cur = self.conn.cursor()
        rows = cur.execute(
            "SELECT name, primary_color, secondary_color, particle_profile, sound_profile FROM custom_powers ORDER BY name"
        ).fetchall()
        return [
            {
                "name": r[0],
                "primary_color": r[1],
                "secondary_color": r[2],
                "particle_profile": r[3],
                "sound_profile": r[4],
            }
            for r in rows
        ]

    def close(self) -> None:
        self.conn.close()
