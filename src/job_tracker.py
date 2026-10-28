"""
Job Application Tracker
Local SQLite persistence for job search workflows and application state.
"""

from __future__ import annotations
import sqlite3
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime, timezone


@dataclass
class TrackedApplication:
    id: Optional[int]
    job_id: str
    title: str
    company: str
    city: str
    status: str  # FOUND, APPLIED, INTERVIEW, OFFER, REJECTED
    applied_date: Optional[str]
    notes: Optional[str]


class JobTrackerDB:
    def __init__(self, db_path: str = "job_applications.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_id TEXT UNIQUE,
                    title TEXT NOT NULL,
                    company TEXT NOT NULL,
                    city TEXT,
                    status TEXT NOT NULL DEFAULT 'FOUND',
                    applied_date TEXT,
                    notes TEXT,
                    updated_at TEXT
                )
                """
            )
            conn.commit()

    def add_job(self, job_id: str, title: str, company: str, city: str, notes: Optional[str] = None):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO applications (job_id, title, company, city, status, updated_at, notes)
                VALUES (?, ?, ?, ?, 'FOUND', ?, ?)
                """,
                (job_id, title, company, city, datetime.now(timezone.utc).isoformat(), notes or ""),
            )
            conn.commit()

    def update_status(self, job_id: str, status: str, notes: Optional[str] = None):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                UPDATE applications
                SET status = ?, notes = coalesce(?, notes), updated_at = ?
                WHERE job_id = ?
                """,
                (status, notes, datetime.now(timezone.utc).isoformat(), job_id),
            )
            conn.commit()

    def list_applications(self, status: Optional[str] = None) -> List[TrackedApplication]:
        with sqlite3.connect(self.db_path) as conn:
            if status:
                cursor = conn.execute(
                    "SELECT id, job_id, title, company, city, status, applied_date, notes FROM applications WHERE status = ?",
                    (status,),
                )
            else:
                cursor = conn.execute(
                    "SELECT id, job_id, title, company, city, status, applied_date, notes FROM applications ORDER BY id DESC"
                )
            return [
                TrackedApplication(
                    id=row[0],
                    job_id=row[1],
                    title=row[2],
                    company=row[3],
                    city=row[4],
                    status=row[5],
                    applied_date=row[6],
                    notes=row[7],
                )
                for row in cursor.fetchall()
            ]
