from __future__ import annotations

import sqlite3
from pathlib import Path


class EngramStore:
    def __init__(self, db_path: str = "engram.db") -> None:
        self.path = Path(db_path)
        self.conn = sqlite3.connect(self.path)
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS episodes (
                id INTEGER PRIMARY KEY,
                content TEXT NOT NULL,
                embedding TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.commit()

    def add_episode(self, content: str, embedding: str | None = None) -> None:
        self.conn.execute(
            "INSERT INTO episodes(content, embedding) VALUES (?, ?)",
            (content, embedding),
        )
        self.conn.commit()
