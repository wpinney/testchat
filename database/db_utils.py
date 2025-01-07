#!/usr/bin/env python3
import sqlite3
from pathlib import Path
from contextlib import contextmanager
from typing import List, Dict, Any, Generator

class DatabaseManager:
    def __init__(self):
        self.db_path = Path(__file__).parent / "db.sqlite"

    @contextmanager
    def get_db(self) -> Generator[sqlite3.Connection, None, None]:
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # This enables column access by name
        try:
            yield conn
        finally:
            conn.close()

    def add_message(self, content: str, sender: str) -> int:
        """Add a new message to the database"""
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO messages (content, sender)
                VALUES (?, ?)
                """,
                (content, sender)
            )
            conn.commit()
            return cursor.lastrowid

    def get_messages(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve recent messages"""
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, content, timestamp, git_hash, sender, is_synced
                FROM messages
                ORDER BY timestamp DESC
                LIMIT ?
                """,
                (limit,)
            )
            return [dict(row) for row in cursor.fetchall()]

    def update_git_hash(self, message_id: int, git_hash: str) -> bool:
        """Update the git hash for a message after syncing"""
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE messages
                SET git_hash = ?, is_synced = 1
                WHERE id = ?
                """,
                (git_hash, message_id)
            )
            conn.commit()
            return cursor.rowcount > 0

    def get_unsynced_messages(self) -> List[Dict[str, Any]]:
        """Get messages that haven't been synced to Git"""
        with self.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, content, timestamp, sender
                FROM messages
                WHERE is_synced = 0
                ORDER BY timestamp ASC
                """
            )
            return [dict(row) for row in cursor.fetchall()]
