import sqlite3

from werkzeug.security import generate_password_hash

DB_PATH = "todos.db"


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_db()
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            title TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    conn.commit()
    conn.close()


def create_user(username: str, password: str) -> int:
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (username, generate_password_hash(password)),
    )
    conn.commit()
    user_id = cur.lastrowid
    conn.close()
    return user_id


def get_user_by_username(username: str):
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()
    conn.close()
    return row


def get_user_by_id(user_id: int):
    conn = get_db()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return row


def list_todos(user_id: int):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM todos WHERE user_id = ? ORDER BY id DESC", (user_id,)
    ).fetchall()
    conn.close()
    return rows


def add_todo(user_id: int, title: str) -> int:
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO todos (user_id, title) VALUES (?, ?)", (user_id, title)
    )
    conn.commit()
    todo_id = cur.lastrowid
    conn.close()
    return todo_id


def get_todo(todo_id: int):
    conn = get_db()
    row = conn.execute("SELECT * FROM todos WHERE id = ?", (todo_id,)).fetchone()
    conn.close()
    return row


def update_todo(todo_id: int, done: bool) -> None:
    conn = get_db()
    conn.execute("UPDATE todos SET done = ? WHERE id = ?", (int(done), todo_id))
    conn.commit()
    conn.close()


def delete_todo(todo_id: int) -> None:
    conn = get_db()
    conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()
