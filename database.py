"""
Database Module
Handles SQLite database operations for storing and retrieving document search history.
"""

import os
import sqlite3
from datetime import datetime
from typing import List, Dict, Any

# Path to SQLite database file
DB_DIR = os.path.join(os.path.dirname(__file__), "database")
DB_PATH = os.path.join(DB_DIR, "documents.db")


def get_connection() -> sqlite3.Connection:
    """
    Creates and returns a connection to the SQLite database.
    Ensures the database directory exists.

    Returns:
        sqlite3.Connection object.
    """
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn


def init_db() -> None:
    """
    Initializes the SQLite database and creates search_history table if not exists.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_name TEXT NOT NULL,
            search_query TEXT NOT NULL,
            top_match_preview TEXT,
            top_score REAL,
            timestamp TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_search_history(
    document_name: str,
    search_query: str,
    top_match_preview: str = "",
    top_score: float = 0.0
) -> None:
    """
    Saves a search query event to the SQLite history table.

    Args:
        document_name: Name of the uploaded PDF file
        search_query: Search query entered by user
        top_match_preview: Short preview snippet of top matching text
        top_score: Similarity score of top match
    """
    conn = get_connection()
    cursor = conn.cursor()

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO search_history (document_name, search_query, top_match_preview, top_score, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (document_name, search_query, top_match_preview[:150], float(top_score), now_str))

    conn.commit()
    conn.close()


def get_search_history(limit: int = 20) -> List[Dict[str, Any]]:
    """
    Retrieves recent search history entries from SQLite database.

    Args:
        limit: Maximum number of recent search records to return.

    Returns:
        List of dictionaries containing search history records.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, document_name, search_query, top_match_preview, top_score, timestamp
        FROM search_history
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    history = [dict(row) for row in rows]
    return history


def clear_search_history() -> None:
    """
    Clears all search history records from SQLite database.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM search_history")
    conn.commit()
    conn.close()
