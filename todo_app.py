"""
TODOアプリのコアロジック。SQLiteで永続化する。
"""

import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "todo.db"


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                title   TEXT    NOT NULL,
                done    INTEGER NOT NULL DEFAULT 0,
                created TEXT    NOT NULL
            )
        """)


def add_todo(title: str) -> int:
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO todos (title, done, created) VALUES (?, 0, ?)",
            (title, datetime.now().isoformat(timespec="seconds")),
        )
        return cur.lastrowid


def list_todos(show_all: bool = False) -> list[sqlite3.Row]:
    with get_conn() as conn:
        if show_all:
            return conn.execute("SELECT * FROM todos ORDER BY id").fetchall()
        return conn.execute(
            "SELECT * FROM todos WHERE done = 0 ORDER BY id"
        ).fetchall()


def mark_done(todo_id: int) -> bool:
    with get_conn() as conn:
        cur = conn.execute(
            "UPDATE todos SET done = 1 WHERE id = ? AND done = 0", (todo_id,)
        )
        return cur.rowcount > 0


def delete_todo(todo_id: int) -> bool:
    with get_conn() as conn:
        cur = conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        return cur.rowcount > 0


def clear_done() -> int:
    with get_conn() as conn:
        cur = conn.execute("DELETE FROM todos WHERE done = 1")
        return cur.rowcount
