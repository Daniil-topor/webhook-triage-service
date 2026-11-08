from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from .models import TriageResult


class AuditStore:
    def __init__(self, path: str = "triage.db") -> None:
        self.path = Path(path)
        connection = self._connect()
        try:
            connection.execute(
                """CREATE TABLE IF NOT EXISTS decisions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                external_id TEXT UNIQUE NOT NULL,
                subject TEXT NOT NULL,
                category TEXT NOT NULL,
                priority TEXT NOT NULL,
                queue TEXT NOT NULL,
                confidence REAL NOT NULL,
                reasons TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )"""
            )
            connection.commit()
        finally:
            connection.close()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.path)

    def save(self, external_id: str, subject: str, result: TriageResult) -> bool:
        connection = self._connect()
        try:
            connection.execute(
                "INSERT INTO decisions (external_id, subject, category, priority, queue, confidence, reasons) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (external_id, subject, result.category, result.priority, result.queue, result.confidence, json.dumps(result.reasons, ensure_ascii=False)),
            )
            connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            connection.close()

    def recent(self, limit: int = 20) -> list[dict]:
        connection = self._connect()
        try:
            connection.row_factory = sqlite3.Row
            rows = connection.execute("SELECT * FROM decisions ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        finally:
            connection.close()
        return [dict(row) for row in rows]
